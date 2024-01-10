from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.metadata import Metadata
from metamorf.tools.query import Query
import os

class EngineUpload(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Upload"
        self.engine_command = "upload"

        self.entry_files_to_load = [FILE_ENTRY_AGGREGATORS, FILE_ENTRY_DATASET_MAPPINGS, FILE_ENTRY_DATASET_RELATIONSHIPS,
                                    FILE_ENTRY_ENTITY, FILE_ENTRY_FILTERS, FILE_ENTRY_ORDER, FILE_ENTRY_PATH,
                                    FILE_ENTRY_HAVING, FILE_ENTRY_DV_ENTITY, FILE_ENTRY_DV_PROPERTIES,
                                    FILE_ENTRY_DV_MAPPINGS, FILE_ENTRY_FILES]
        if 'select' in self.arguments:
            if self.arguments['select'] == "all" or self.arguments['select'] == "*":
                self.entry_files_to_load = [FILE_ENTRY_AGGREGATORS, FILE_ENTRY_DATASET_MAPPINGS, FILE_ENTRY_DATASET_RELATIONSHIPS,
                                            FILE_ENTRY_ENTITY, FILE_ENTRY_FILTERS, FILE_ENTRY_ORDER, FILE_ENTRY_PATH,
                                            FILE_ENTRY_HAVING, FILE_ENTRY_DV_ENTITY, FILE_ENTRY_DV_PROPERTIES,
                                            FILE_ENTRY_DV_MAPPINGS, FILE_ENTRY_FILES]
            if self.arguments['select'].lower() == FILE_ENTRY_DATASET_MAPPINGS.lower():
                self.entry_files_to_load = [FILE_ENTRY_DATASET_MAPPINGS]
            if self.arguments['select'].lower() == FILE_ENTRY_DATASET_RELATIONSHIPS.lower():
                self.entry_files_to_load = [FILE_ENTRY_DATASET_RELATIONSHIPS]
            if self.arguments['select'].lower() == FILE_ENTRY_ENTITY.lower():
                self.entry_files_to_load = [FILE_ENTRY_ENTITY]
            if self.arguments['select'].lower() == FILE_ENTRY_FILTERS.lower():
                self.entry_files_to_load = [FILE_ENTRY_FILTERS]
            if self.arguments['select'].lower() == FILE_ENTRY_ORDER.lower():
                self.entry_files_to_load = [FILE_ENTRY_ORDER]
            if self.arguments['select'].lower() == FILE_ENTRY_PATH.lower():
                self.entry_files_to_load = [FILE_ENTRY_PATH]
            if self.arguments['select'].lower() == FILE_ENTRY_HAVING.lower():
                self.entry_files_to_load = [FILE_ENTRY_HAVING]
            if self.arguments['select'].lower() == FILE_ENTRY_DV_ENTITY.lower():
                self.tables_to_load = [FILE_ENTRY_DV_ENTITY]
            if self.arguments['select'].lower() == FILE_ENTRY_DV_PROPERTIES.lower():
                self.tables_to_load = [FILE_ENTRY_DV_PROPERTIES]
            if self.arguments['select'].lower() == FILE_ENTRY_DV_MAPPINGS.lower():
                self.tables_to_load = [FILE_ENTRY_DV_MAPPINGS]
            if self.arguments['select'].lower() == FILE_ENTRY_FILES.lower():
                self.tables_to_load = [FILE_ENTRY_FILES]


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
        self.log.log(self.engine_name, "Starting deleting Metadata Entry on database" , LOG_LEVEL_INFO)
        connection_type = self.configuration['metadata']['connection_type']
        for file in self.entry_files_to_load:
            self.log.log(self.engine_name, "Deleting: " + file, LOG_LEVEL_INFO)
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(file)
            query.set_where_filters([COLUMN_ENTRY_OWNER + "='" + self.owner + "'"])
            res = self.connection.execute(str(query))
            result = result and res
        self.log.log(self.engine_name, "Finished deleting Metadata Entry on database", LOG_LEVEL_INFO)
        return result

    def add_owner_at_end_each_row(self, file: list[list]):
        result = []
        for f in file:
            s = f
            s.append(self.configuration['owner'])
            result.append(s)
        return result

    def load_files_to_metadata_database(self):
        self.log.log(self.engine_name, "Starting uploading Metadata Entry on database", LOG_LEVEL_INFO)
        result = True
        metadata = Metadata(self.log)
        connection_type = self.configuration['metadata']['connection_type']

        # ENTRY_AGGREGATORS
        if FILE_ENTRY_AGGREGATORS in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH),
                                          FILE_ENTRY_AGGREGATORS + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()

            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_aggregators(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_AGGREGATORS)
            query_values.set_insert_columns(COLUMNS_ENTRY_AGGREGATORS)
            query_values.set_values(metadata.entry_aggregators)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_AGGREGATORS, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_DATASET_MAPPINGS
        if FILE_ENTRY_DATASET_MAPPINGS in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH),
                                          FILE_ENTRY_DATASET_MAPPINGS + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_dataset_mappings(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_DATASET_MAPPINGS)
            query_values.set_insert_columns(COLUMNS_ENTRY_DATASET_MAPPINGS)
            query_values.set_values(metadata.entry_dataset_mappings)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_DATASET_MAPPINGS, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_DATASET_RELATIONSHIPS
        if FILE_ENTRY_DATASET_RELATIONSHIPS in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH),
                                          FILE_ENTRY_DATASET_RELATIONSHIPS + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_dataset_relationship(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_DATASET_RELATIONSHIPS)
            query_values.set_insert_columns(COLUMNS_ENTRY_DATASET_RELATIONSHIPS)
            query_values.set_values(metadata.entry_dataset_relationship)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_DATASET_RELATIONSHIPS, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_ENTITY
        if FILE_ENTRY_ENTITY in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_ENTITY + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_entity(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_ENTITY)
            query_values.set_insert_columns(COLUMNS_ENTRY_ENTITY)
            query_values.set_values(metadata.entry_entity)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_ENTITY, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_FILTERS
        if FILE_ENTRY_FILTERS in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_FILTERS + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_filters(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_FILTERS)
            query_values.set_insert_columns(COLUMNS_ENTRY_FILTERS)
            query_values.set_values(metadata.entry_filters)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_FILTERS, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_HAVING
        if FILE_ENTRY_HAVING in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH),
                                          FILE_ENTRY_HAVING + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_having(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_HAVING)
            query_values.set_insert_columns(COLUMNS_ENTRY_HAVING)
            query_values.set_values(metadata.entry_having)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_HAVING, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_ORDER
        if FILE_ENTRY_ORDER in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_ORDER + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_order(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_ORDER)
            query_values.set_insert_columns(COLUMNS_ENTRY_ORDER)
            query_values.set_values(metadata.entry_order)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_ORDER, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_PATH
        if FILE_ENTRY_PATH in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_PATH + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_path(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_PATH)
            query_values.set_insert_columns(COLUMNS_ENTRY_PATH)
            query_values.set_values(metadata.entry_path)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_PATH, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_DV_ENTITY
        if FILE_ENTRY_DV_ENTITY in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH),
                                          FILE_ENTRY_DV_ENTITY + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_dv_entity(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_DV_ENTITY)
            query_values.set_insert_columns(COLUMNS_ENTRY_DV_ENTITY)
            query_values.set_values(metadata.entry_dv_entity)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_DV_ENTITY, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_DV_MAPPINGS
        if FILE_ENTRY_DV_MAPPINGS in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_DV_MAPPINGS + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_dv_mappings(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_DV_MAPPINGS)
            query_values.set_insert_columns(COLUMNS_ENTRY_DV_MAPPINGS)
            query_values.set_values(metadata.entry_dv_mappings)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_DV_MAPPINGS, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_DV_PROPERTIES
        if FILE_ENTRY_DV_PROPERTIES in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH),
                                          FILE_ENTRY_DV_PROPERTIES + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_dv_properties(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_DV_PROPERTIES)
            query_values.set_insert_columns(COLUMNS_ENTRY_DV_PROPERTIES)
            query_values.set_values(metadata.entry_dv_properties)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_DV_PROPERTIES, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        # ENTRY_FILES
        if FILE_ENTRY_FILES in self.entry_files_to_load:
            file_reader = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_reader.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH),
                                          FILE_ENTRY_FILES + "." + FILE_TYPE_CSV)
            file = file_reader.read_file()
            all_rows = self.add_owner_at_end_each_row(file)
            res = metadata.add_entry_files(all_rows)
            result = result and res
            query_values = Query()
            query_values.set_database(connection_type)
            query_values.set_has_header(True)
            query_values.set_type(QUERY_TYPE_VALUES)
            query_values.set_target_table(TABLE_ENTRY_FILES)
            query_values.set_insert_columns(COLUMNS_ENTRY_FILES)
            query_values.set_values(metadata.entry_files)
            self.log.log(self.engine_name, "Loading: " + TABLE_ENTRY_FILES, LOG_LEVEL_INFO)
            res = self.connection.execute(str(query_values))
            result = result and res

        self.log.log(self.engine_name, "Finished uploading Metadata Entry on database", LOG_LEVEL_INFO)
        return result
