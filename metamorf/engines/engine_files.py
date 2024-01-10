from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.metadata import Metadata
from metamorf.tools.query import Query
import glob
import os

class EngineFiles(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Files"
        self.engine_command = "files"


    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()
        self.connection_type = self.configuration['data']['connection_type']
        self.connection_data = ConnectionFactory().get_connection(self.configuration['data']['connection_type'])
        self.connection_metadata = ConnectionFactory().get_connection(self.configuration['metadata']['connection_type'])
        self.connection_metadata.setup_connection(self.configuration['metadata'], self.log)
        self.metadata_actual = self.load_metadata(load_om=False, load_entry=True, load_ref=False, load_im=False, owner=self.owner)
        self.metadata_to_load = Metadata(self.log)

        result = self.load_files_to_data_database()
        super().finish_execution(result)


    def load_files_to_data_database(self):
        self.log.log(self.engine_name, "Starting to upload files", LOG_LEVEL_INFO)
        result = True
        for file in self.metadata_actual.entry_files:

            self.log.log(self.engine_name, "Starting to upload ['"+str(os.path.join(file.file_path , file.file_name))+"'] file", LOG_LEVEL_INFO)

            entry_entity = self.metadata_actual.get_entry_entity_from_cod_entity(file.cod_entity)

            path_entity = self.metadata_actual.get_entry_path_from_cod_path(entry_entity.cod_path)
            # Prepare connection path
            new_connection = self.connection_data.get_configuarion_of_connection_on_path(self.configuration['data'], path_entity.database_name, path_entity.schema_name)
            self.connection_data.setup_connection(new_connection, self.log)

            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_delimiter(file.delimiter_character)

            file_list = glob.glob(os.path.join(file.file_path,file.file_name))

            all_rows = []
            header = []
            is_header = True
            first_time = False
            for f in file_list:
                file_reader.set_file_location(None, f)
                file_content = file_reader.read_file()
                if file_content is None:
                    self.log.log(self.engine_name, "The file ['" + str(os.path.join(file.file_path , file.file_name)) + "'] has not been found", LOG_LEVEL_WARNING)
                    return result
                for row in file_content:
                    if first_time:
                        first_time = False
                        continue
                    if is_header:
                        header = row
                        is_header = False
                    new_row = ''
                    for pos in row:
                        new_row += "'" + pos.replace("'","''") + "',"
                    all_rows.append(new_row[:-1])
                first_time = True

            columns_and_specs = []
            for r in header:
                new_column = r + " " + self.connection_data.get_string_for_metadata()[0]
                columns_and_specs.append(new_column)

            table_exists = self.connection_data.does_table_exists(entry_entity.table_name, path_entity.schema_name, path_entity.database_name)

            query_values = Query()
            query_values.set_need_drop_table(table_exists)
            query_values.set_need_create_table(True)
            query_values.set_database(self.connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(entry_entity.table_name)
            query_values.set_insert_columns(header)
            query_values.set_columns_and_specs(columns_and_specs)
            query_values.set_values(all_rows)

            self.connection_data.execute(str(query_values))
            self.connection_data.commit()

            self.log.log(self.engine_name, "The file ['" + str(os.path.join(file.file_path, file.file_name)) + "'] has been uploaded", LOG_LEVEL_INFO)

        self.log.log(self.engine_name, "Finished to upload files", LOG_LEVEL_INFO)

        return result
