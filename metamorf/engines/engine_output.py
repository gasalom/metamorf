from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.utils import get_list_nodes_from_metadata, get_node_with_with_query_execution_settings
import re

class EngineOutput(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Output"
        self.engine_command = "output"

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()

        output_type = self.configuration_file['output']['type']

        self.metadata = self.load_metadata(load_om=True, load_ref=True, load_entry=False, load_im=False, owner=self.owner)

        all_nodes = get_list_nodes_from_metadata(self.metadata, self.log, "all")

        self.log.log(self.engine_name, "Start to Generate Files with [" + output_type + "] configuration", LOG_LEVEL_INFO)

        connection_type = self.configuration_file['metadata']['connection_type']
        connection = ConnectionFactory().get_connection(connection_type)

        for node in all_nodes:

            path = self.metadata.get_path_from_dataset_name(node.name)
            configuration = self.configuration_file['data']
            configuration[connection_type + "_database"] = path.database_name
            configuration[connection_type + "_schema"] = path.schema_name
            connection.setup_connection(configuration, self.log)

            # Select Strategy of Materialization
            if output_type.upper() == OUTPUT_TYPE_DBT.upper():
                node.query.set_type(QUERY_TYPE_SELECT)
                content = str(node.query)
                content = self.dbt_create_config_for_models(node) + "\n\n" + content
                for table in node.predecessors:
                    dataset = self.metadata.get_dataset_from_dataset_name(table)
                    fqdn = self.metadata.get_dataset_fqdn_from_dataset_name(table)
                    if dataset.id_entity_type == self.metadata.get_entity_type_from_entity_type_name(ENTITY_SRC).id_entity_type:
                        path = self.metadata.get_path_from_id_path(dataset.id_path)
                        content = re.sub("\s+"+fqdn+"\s+|\r", " {{source('"+self.get_source_dbt_name_from_path(path)+"','"+table+"')}} ", content )
                    else:
                        content = re.sub("\s+" + fqdn + "\s|\r+", " {{ref('" + table + "')}} ", content)

            else:
                node = get_node_with_with_query_execution_settings(connection, self.metadata, node)
                content = str(node.query)


            file_controller = FileControllerFactory().get_file_reader(FILE_TYPE_SQL)
            file_controller.set_file_location(ACTUAL_PATH + '\\' + OUTPUT_FILES_PATH, node.name)
            file_controller.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller.write_file(content)


        # Create source files for DBT
        if output_type.upper() == OUTPUT_TYPE_DBT.upper():
            self.dbt_create_source_yml()

        self.log.log(self.engine_name, "Finish Generate Files", LOG_LEVEL_INFO)
        super().finish_execution()

    def get_source_dbt_name_from_path(self, path):
        return 'metamorf' + self.get_fqdn_from_path(path)

    def get_fqdn_from_path(self, path):
        fqdn = ""
        if path.database_name is None or path.database_name == "":
            if path.schema_name is not None and path.schema_name != "":
                fqdn = "_" + path.schema_name
        else:
            if path.schema_name is None or path.schema_name == "":
                fqdn = "_" + path.database_name
            else:
                fqdn = "_" + path.database_name + "_" + path.schema_name
        return fqdn

    def get_paths_with_sources(self):
        path_with_source = []
        for dataset in self.metadata.om_dataset:
            if dataset.end_date is not None: continue
            if dataset.id_entity_type == self.metadata.get_entity_type_from_entity_type_name(ENTITY_SRC).id_entity_type:
                possible_path = self.metadata.get_path_from_id_path(dataset.id_path)
                if possible_path not in path_with_source:
                    path_with_source.append(possible_path)
        return path_with_source

    def get_sources_from_path(self, path):
        sources = []
        for dataset in self.metadata.om_dataset:
            if dataset.end_date is not None: continue
            if dataset.id_path == path.id_path and dataset.id_entity_type == self.metadata.get_entity_type_from_entity_type_name(ENTITY_SRC).id_entity_type:
                sources.append(dataset.dataset_name)
        return sources

    def dbt_create_source_yml(self):
        paths_with_sources = self.get_paths_with_sources()
        # Get all Paths with Sources
        yml_content = dict()
        yml_content['version'] = 2
        yml_content['sources'] = []

        for path in paths_with_sources:
            yml_name = dict()
            yml_name['name'] = self.get_source_dbt_name_from_path(path)
            yml_name['description'] = "Source generated by Metamorf"
            if path.database_name is not None and path.database_name != '':
                yml_name['database'] = path.database_name
            if path.schema_name is not None and path.schema_name != '':
                yml_name['schema'] = path.schema_name
            yml_name['tables'] = []
            all_sources_from_path = self.get_sources_from_path(path)

            for src in all_sources_from_path:
                yml_table = dict()
                yml_table['name'] = src
                yml_name['tables'].append(yml_table)

            yml_content['sources'].append(yml_name)

        file_controller = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
        file_controller.set_file_location(ACTUAL_PATH + '\\' + OUTPUT_FILES_PATH, "sources_metamorf")
        file_controller.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller.write_file(yml_content)

    def dbt_create_config_for_models(self, node):
        id_query_type = self.metadata.get_dataset_execution_from_id_dataset(self.metadata.get_dataset_from_dataset_name(node.name).id_dataset).id_query_type
        config = "{{ config(materialized='"
        #TODO: Add more options to config DBT
        if id_query_type == QUERY_TYPE_TRUNCATE_AND_INSERT: config += "table"
        if id_query_type == QUERY_TYPE_INSERT or id_query_type == QUERY_TYPE_UPDATE: config += "incremental'"
        if id_query_type == QUERY_TYPE_VIEW: config += "view'"
        if id_query_type == QUERY_TYPE_MERGE:
            all_pk = []
            dataset_id = self.metadata.get_dataset_from_dataset_name(node.name).id_dataset
            for dataset_spec in self.metadata.om_dataset_specification:
                if dataset_spec.end_date is not None: continue
                if dataset_spec.id_dataset == dataset_id and dataset_spec.id_key_type == self.metadata.get_key_type_from_key_type_name(KEY_TYPE_PRIMARY_KEY).id_key_type:
                    all_pk.append(dataset_spec.column_name)

            config += "incremental', unique_key=["
            for pk in all_pk:
                config += "'"+pk+"'" +","
            config = config[:-1]
            config+= "]"
        config += ")}}"
        return config
