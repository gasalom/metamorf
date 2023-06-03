import concurrent.futures

from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.utils import get_list_nodes_from_metadata, get_node_with_with_query_execution_settings
import threading

class EngineRun(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Run"
        self.engine_command = "run"

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()

        self.metadata = self.load_metadata(load_om=True, load_ref=True, load_entry=False, load_im=False, owner=self.owner)
        #TODO: Actually it executes all the project of the owner -> "all"
        nodes = get_list_nodes_from_metadata(self.metadata, self.log, "all")

        connection_type = self.configuration_file['metadata']['connection_type']
        connection = ConnectionFactory().get_connection(connection_type)

        process_finished_ok = []
        process_finished_nok = []
        for dataset in self.metadata.om_dataset:
            if dataset.id_entity_type == self.metadata.get_entity_type_from_entity_type_name(ENTITY_SRC).id_entity_type:
                process_finished_ok.append(dataset.dataset_name)

        self.log.log(self.engine_name, "Start the execution", LOG_LEVEL_INFO)
        index = 0
        results_nodes = []
        while nodes:
            node = nodes[index]
            if(set(node.predecessors).issubset(process_finished_ok)):
                node.init_execution()
                node.status = NODE_STATUS_RUNNING
                result_execution = self.execute_node(node, connection)
                if result_execution:
                    node.status = NODE_STATUS_FINISHED_OK
                    process_finished_ok.append(node.name)

                else:
                    node.status = NODE_STATUS_FINISHED_NOK
                    process_finished_nok.append(node.name)

                node.finish_execution()
                results_nodes.append(node)
                nodes.remove(node)

            elif(set(node.predecessors).issubset(process_finished_ok + process_finished_nok)):
                node.status = NODE_STATUS_SKIP
                process_finished_nok.append(node.name)
                results_nodes.append(node)
                nodes.remove(node)

            index += 1
            if index>=len(nodes): index = 0

        self.log.log(self.engine_name, "Finish the execution", LOG_LEVEL_INFO)
        if len(self.metadata.om_dataset)==0:
            self.log.log(self.engine_name, "There is no nodes to execute", LOG_LEVEL_WARNING)
        else: self.show_results(results_nodes)
        super().finish_execution()

    def show_results(self, nodes):
        self.log.log("RESULT EXECUTION", "**********************************************", LOG_LEVEL_INFO)
        self.log.log("RESULT EXECUTION", "Summary of the execution", LOG_LEVEL_INFO)
        for node in nodes:
            if node.status == NODE_STATUS_FINISHED_OK:
                self.log.log("RESULT EXECUTION", node.name + " --> Finished Ok in [" + "{:.3f}".format(node.time) + " seconds]", LOG_LEVEL_OK)
            if node.status == NODE_STATUS_FINISHED_NOK:
                self.log.log("RESULT EXECUTION", node.name + " --> Finished Not Ok in [" + "{:.3f}".format(node.time) + " seconds]", LOG_LEVEL_ERROR)
            if node.status == NODE_STATUS_SKIP:
                self.log.log("RESULT EXECUTION", node.name + " --> Skipped because a predecessor finished not ok", LOG_LEVEL_WARNING)
        self.log.log("RESULT EXECUTION", "**********************************************", LOG_LEVEL_INFO)

    def execute_node(self, node, connection):
        self.log.log(self.engine_name, "Start executing " + node.name, LOG_LEVEL_INFO)

        path = self.metadata.get_path_from_dataset_name(node.name)
        connection_type = self.configuration_file['metadata']['connection_type']
        configuration = self.configuration_file['data']
        configuration[connection_type + "_database"] = path.database_name
        configuration[connection_type + "_schema"] = path.schema_name
        connection.setup_connection(configuration,self.log)

        # Select Strategy of Materialization
        node = get_node_with_with_query_execution_settings(connection, self.metadata, node)

        result_execution = connection.execute(str(node.query))
        connection.commit()

        self.log.log(self.engine_name, "Finished " + node.name, LOG_LEVEL_INFO)

        return result_execution