import concurrent.futures

from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.utils import get_list_nodes_from_metadata, get_node_with_with_query_execution_settings
import threading
from threading import Lock

class EngineRun(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Run"
        self.engine_command = "run"

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()

        self.metadata = self.load_metadata(load_om=True, load_ref=True, load_entry=False, load_im=False, owner=self.owner)

        process_finished_ok = []
        process_finished_nok = []
        for dataset in self.metadata.om_dataset:
            if dataset.id_entity_type == self.metadata.get_entity_type_from_entity_type_name(ENTITY_SRC).id_entity_type:
                process_finished_ok.append(dataset.dataset_name)

        nodes = get_list_nodes_from_metadata(self.metadata, self.log)
        for node in nodes:
            node.query.set_database(self.configuration['data']['connection_type'].upper())

        # Create Databases and Schemas if not exists
        self._create_databases_and_schemas(self.configuration['data'])

        target_node_name = None
        to_final_flag = False
        if 'select' in self.arguments:
            target_node_name = self.arguments['select']
            if target_node_name[-1]=='+':
                to_final_flag = True
                target_node_name = target_node_name[:-1]

        if target_node_name is not None:
            self.log.log(self.engine_name, "The execution will start from [" + target_node_name + "]", LOG_LEVEL_ONLY_LOG)
            if to_final_flag:
                self.log.log(self.engine_name, "The execution will continue to the sucessors from [" + target_node_name + "]", LOG_LEVEL_ONLY_LOG)
            target_node,nodes = self.get_all_nodes_filtered(nodes, target_node_name, to_final_flag)
            if target_node is not None:
                for predecessor in target_node.predecessors:
                    process_finished_ok.append(predecessor)
            if target_node is None:
                self.log.log(self.engine_name, "There is no entity with this name [" + target_node_name + "]", LOG_LEVEL_ERROR)

        lock = Lock()
        max_threads = min(self.configuration['modules']['elt']['threads'], len(nodes))
        self.log.log(self.engine_name, "Start the execution with [" + str(max_threads) + "] threads", LOG_LEVEL_INFO)
        results_nodes = []

        all_threads = []
        self.total_nodes = len(nodes)
        self.actual = 0
        self.need_to_stop = False

        for idx,thread in enumerate(range(max_threads)):
            all_threads.append(threading.Thread(target=self.thread_for_execute_nodes, args = (nodes,process_finished_ok, process_finished_nok, results_nodes, lock, idx)))
        for thread in all_threads: thread.start()
        for thread in all_threads: thread.join()

        self.log.log(self.engine_name, "Finish the execution", LOG_LEVEL_INFO)
        if len(self.metadata.om_dataset)==0:
            self.log.log(self.engine_name, "There is no nodes to execute", LOG_LEVEL_WARNING)
        else: self.show_results(results_nodes)
        super().finish_execution()

    def get_all_nodes_filtered(self, nodes, target_node_name, to_final=False):
        nodes_to_execute = []
        target_node = None
        for node in nodes:
            if node.name == target_node_name:
                nodes_to_execute.append(node)
                target_node = node

        if not to_final: return target_node,nodes_to_execute

        all_tables_ok = []
        all_tables_ok.append(target_node.name)

        while True:
            all_new_nodes = self.return_all_nodes_that_can_be_executed(nodes, nodes_to_execute, all_tables_ok)
            for n in all_new_nodes:
                nodes_to_execute.append(n)
            if len(all_new_nodes)==0: break

        return target_node,nodes_to_execute

    def return_all_nodes_that_can_be_executed(self, all_nodes, nodes_ok, all_tables_ok):
        new_nodes = []
        for node in all_nodes:
            if set(node.predecessors).issubset(all_tables_ok) and node not in nodes_ok:
                new_nodes.append(node)
        return new_nodes

    def thread_for_execute_nodes(self, all_nodes_to_execute, process_finished_ok, process_finished_nok, results_nodes, lock, thread_num):
        index = -1
        connection = ConnectionFactory().get_connection(self.configuration['data']['connection_type'])
        need_to_execute = False
        num_node_next_execution = 0
        while all_nodes_to_execute:
            if self.need_to_stop: return
            lock.acquire()

            index += 1
            if index >= len(all_nodes_to_execute): index = 0
            if len(all_nodes_to_execute)<=0:
                lock.release()
                return
            node = all_nodes_to_execute[index]
            if(set(node.predecessors).issubset(process_finished_ok)) and node.status == NODE_STATUS_WAITING:
                need_to_execute = True
                self.actual += 1
                num_node_next_execution = self.actual
                node.init_execution()
                node.status = NODE_STATUS_RUNNING
            elif (set(node.predecessors).issubset(process_finished_ok + process_finished_nok)) and node.status == NODE_STATUS_WAITING:
                node.status = NODE_STATUS_SKIP
                self.actual += 1
                num_node_next_execution = self.actual
                process_finished_nok.append(node.name)
                results_nodes.append(node)
                all_nodes_to_execute.remove(node)
            lock.release()

            if need_to_execute:
                result_execution = self.execute_node(node, connection, thread_num, num_node_next_execution)
                lock.acquire()
                if result_execution:
                    node.status = NODE_STATUS_FINISHED_OK
                    process_finished_ok.append(node.name)
                else:
                    node.status = NODE_STATUS_FINISHED_NOK
                    process_finished_nok.append(node.name)
                    if self.configuration['modules']['elt']['execution'] == CONFIG_EXECUTION_STOP_ON_ERRORS:
                        self.need_to_stop = True
                        self.log.log(self.engine_name, "No other process will be executed", LOG_LEVEL_ERROR)
                node.finish_execution()
                results_nodes.append(node)
                all_nodes_to_execute.remove(node)
                lock.release()

            need_to_execute = False

    def show_results(self, nodes):
        self.log.log("Result Execution", "**********************************************", LOG_LEVEL_INFO)
        self.log.log("Result Execution", "Summary of the execution", LOG_LEVEL_INFO)
        for node in nodes:
            if node.status == NODE_STATUS_FINISHED_OK:
                self.log.log("Result Execution", node.name + " --> Finished Ok in [" + "{:.3f}".format(node.time) + " seconds]", LOG_LEVEL_OK)
            if node.status == NODE_STATUS_FINISHED_NOK:
                self.log.log("Result Execution", node.name + " --> Finished Not Ok in [" + "{:.3f}".format(node.time) + " seconds]", LOG_LEVEL_ERROR)
            if node.status == NODE_STATUS_SKIP:
                self.log.log("Result Execution", node.name + " --> Skipped because a predecessor finished not ok", LOG_LEVEL_WARNING)
        self.log.log("Result Execution", "**********************************************", LOG_LEVEL_INFO)

    def execute_node(self, node, connection, thread_num, actual_execution):
        self.log.log(self.engine_name, "Thread ["+str(thread_num)+"] Process ["+str(actual_execution)+"/"+str(self.total_nodes)+"] Start executing " + node.name, LOG_LEVEL_INFO)

        path = self.metadata.get_path_from_dataset_name(node.name)
        configuration = connection.get_configuarion_of_connection_on_path(self.configuration['data'], path.database_name, path.schema_name)
        connection.setup_connection(configuration,self.log)

        # Select Strategy of Materialization
        node = get_node_with_with_query_execution_settings(connection, self.metadata, node, self.configuration)

        result_execution = connection.execute(str(node.query))
        connection.commit()

        self.log.log(self.engine_name, "Thread ["+str(thread_num)+"] Process ["+str(actual_execution)+"/"+str(self.total_nodes)+"] Finished " + node.name, LOG_LEVEL_INFO)

        return result_execution

    def _create_databases_and_schemas(self, configuration):
        self.log.log(self.engine_name, "Checking if all databases and schemas exist", LOG_LEVEL_INFO)

        connection = ConnectionFactory().get_connection(configuration['connection_type'])
        connection.setup_connection(configuration, self.log)
        all_databases_needed = connection.get_databases_available()

        for path in [x for x in self.metadata.om_dataset_path if x.end_date is None or x.end_date == '']:

            if configuration['connection_type'] in (CONNECTION_SQLITE): continue
            connection.setup_connection(configuration, self.log)
            # Create Database
            if path.database_name not in all_databases_needed:
                self.log.log(self.engine_name, "Creating Database [" + path.database_name + "]", LOG_LEVEL_INFO)
                result_database = connection.create_database(path.database_name)
                if not result_database:
                    self.log.log(self.engine_name, "Database [" + path.schema_name + "] could not be created", LOG_LEVEL_ERROR)
                else:
                    connection.commit()
                    self.log.log(self.engine_name, "Database [" + path.schema_name + "] created", LOG_LEVEL_INFO)

            # Create Schema
            if configuration['connection_type'] in (CONNECTION_MYSQL): continue
            configuration_tmp = connection.get_configuarion_of_connection_on_path(configuration, path.database_name, path.schema_name)
            connection.setup_connection(configuration_tmp, self.log)
            all_schemas_needed = connection.get_schemas_available()
            if path.schema_name not in all_schemas_needed:
                self.log.log(self.engine_name, "Creating schema [" + path.schema_name + "]", LOG_LEVEL_INFO)
                result_schemas = connection.create_schema(path.schema_name)
                if not result_schemas:
                    self.log.log(self.engine_name, "Schema [" + path.schema_name + "] could not be created", LOG_LEVEL_ERROR)
                else:
                    connection.commit()
                    self.log.log(self.engine_name, "Schema [" + path.schema_name + "] created", LOG_LEVEL_INFO)

        connection.close()
        self.log.log(self.engine_name, "Finished to check if all databases and schemas exist", LOG_LEVEL_INFO)
