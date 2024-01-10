from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.metadata import Metadata
from metamorf.tools.query import Query
import os

class EngineRestore(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Restore"
        self.engine_command = "restore"

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()
        connection_type = self.configuration['metadata']['connection_type']
        self.connection = ConnectionFactory().get_connection(connection_type)
        self.connection.setup_connection(self.configuration['metadata'], self.log)

        result_delete = self.delete_all_entry_from_owner()
        if not result_delete:
            self.connection.rollback()
            super().finish_execution(result_delete)
        else:
            result = self.load_files_to_metadata_database()
            if not result: self.connection.rollback()
            else: self.connection.commit()
            super().finish_execution(result)

    def delete_all_entry_from_owner(self):
        result = True
        self.log.log(self.engine_name, "Starting deleting Metadata on database" , LOG_LEVEL_INFO)
        connection_type = self.configuration['metadata']['connection_type']
        metadata_tables = [TABLE_OM_DATASET, TABLE_OM_DATASET_EXECUTION, TABLE_OM_DATASET_T_ORDER,
                           TABLE_OM_DATASET_T_AGG, TABLE_OM_DATASET_T_DISTINCT, TABLE_OM_DATASET_SPECIFICATION,
                           TABLE_OM_DATASET_RELATIONSHIPS, TABLE_OM_DATASET_T_MAPPING, TABLE_OM_DATASET_T_FILTER,
                           TABLE_OM_DATASET_T_HAVING, TABLE_OM_DATASET_PATH , TABLE_OM_PROPERTIES, TABLE_OM_DATASET_DV]
        for file in metadata_tables:
            self.log.log(self.engine_name, "Deleting: " + file, LOG_LEVEL_INFO)
            query = Query()
            query.set_database(connection_type)
            query.set_target_table(file)
            query.set_is_truncate(True)
            res = self.connection.execute(str(query))
            result = result and res
        return result

    def refactor_file(self, file):
        for row in file:
            row[len(row)-2] = "'"+row[len(row)-2] +"'"
            if row[len(row)-1] is not None and row[len(row)-1] != '': row[len(row)-1] = "'"+ row[len(row)-1] + "'"
        return file

    def refactor_file_last_col(self, file):
        for row in file:
            row[len(row)-1] = "'"+row[len(row)-1] + "'"
        return file

    def load_files_to_metadata_database(self):
        self.log.log(self.engine_name, "Starting uploading Metadata Entry on database", LOG_LEVEL_INFO)
        result = True
        metadata = Metadata(self.log)
        connection_type = self.configuration['metadata']['connection_type']

        # TABLE_OM_DATASET
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH), TABLE_OM_DATASET + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET)
        query_values.set_insert_columns(COLUMNS_OM_DATASET)
        query_values.set_values(metadata.om_dataset)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_DV
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH), TABLE_OM_DATASET_DV + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_dv(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_DV)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_DV)
        query_values.set_values(metadata.om_dataset_dv)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_DV, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_EXECUTION
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH), TABLE_OM_DATASET_EXECUTION + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_execution(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_EXECUTION)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_EXECUTION)
        query_values.set_values(metadata.om_dataset_execution)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_EXECUTION, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_T_ORDER
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH), TABLE_OM_DATASET_T_ORDER + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_t_order(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_T_ORDER)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_T_ORDER)
        query_values.set_values(metadata.om_dataset_t_order)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_T_ORDER, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_T_AGG
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH), TABLE_OM_DATASET_T_AGG + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_t_agg(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_T_AGG)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_T_AGG)
        query_values.set_values(metadata.om_dataset_t_agg)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_T_AGG, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_T_DISTINCT
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH),
                                      TABLE_OM_DATASET_T_DISTINCT + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_t_distinct(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_T_DISTINCT)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_T_DISTINCT)
        query_values.set_values(metadata.om_dataset_t_distinct)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_T_DISTINCT, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_SPECIFICATION
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH),
                                      TABLE_OM_DATASET_SPECIFICATION + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_specification(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_SPECIFICATION)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_SPECIFICATION)
        query_values.set_values(metadata.om_dataset_specification)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_SPECIFICATION, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_RELATIONSHIPS
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH),
                                      TABLE_OM_DATASET_RELATIONSHIPS + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_relationships(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_RELATIONSHIPS)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_RELATIONSHIPS)
        query_values.set_values(metadata.om_dataset_relationships)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_RELATIONSHIPS, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_T_MAPPING
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH),
                                      TABLE_OM_DATASET_T_MAPPING + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_t_mapping(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_T_MAPPING)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_T_MAPPING)
        query_values.set_values(metadata.om_dataset_t_mapping)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_T_MAPPING, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_T_FILTER
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH),
                                      TABLE_OM_DATASET_T_FILTER + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_t_filter(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_T_FILTER)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_T_FILTER)
        query_values.set_values(metadata.om_dataset_t_filter)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_T_FILTER, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_T_HAVING
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH),
                                      TABLE_OM_DATASET_T_HAVING + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_t_having(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_T_HAVING)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_T_HAVING)
        query_values.set_values(metadata.om_dataset_t_having)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_T_HAVING, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_DATASET_PATH
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH),
                                      TABLE_OM_DATASET_PATH + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_dataset_path(self.refactor_file(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_DATASET_PATH)
        query_values.set_insert_columns(COLUMNS_OM_DATASET_PATH)
        query_values.set_values(metadata.om_dataset_path)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_DATASET_PATH, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res

        # TABLE_OM_PROPERTIES
        file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_reader.set_file_location(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH),
                                      TABLE_OM_PROPERTIES + "." + FILE_TYPE_CSV)
        file = file_reader.read_file()
        res = metadata.add_om_properties(self.refactor_file_last_col(file))
        result = result and res
        query_values = Query()
        query_values.set_database(connection_type)
        query_values.set_has_header(True)
        query_values.set_type(QUERY_TYPE_VALUES)
        query_values.set_target_table(TABLE_OM_PROPERTIES)
        query_values.set_insert_columns(COLUMNS_OM_PROPERTIES)
        query_values.set_values(metadata.om_properties)
        self.log.log(self.engine_name, "Loading: " + TABLE_OM_PROPERTIES, LOG_LEVEL_INFO)
        res = self.connection.execute(str(query_values))
        result = result and res



        return result
