from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.query import Query

class EngineRecover(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Recover"
        self.engine_command = "recover"

        self.tables_to_load = [TABLE_ENTRY_AGGREGATORS, TABLE_ENTRY_DATASET_MAPPINGS,
                               TABLE_ENTRY_DATASET_RELATIONSHIPS, TABLE_ENTRY_ENTITY, TABLE_ENTRY_FILTERS,
                               TABLE_ENTRY_ORDER, TABLE_ENTRY_PATH, TABLE_ENTRY_HAVING,
                               TABLE_ENTRY_DV_ENTITY, TABLE_ENTRY_DV_MAPPINGS, TABLE_ENTRY_DV_PROPERTIES,
                               TABLE_ENTRY_FILES]
        if 'select' in self.arguments:
            if self.arguments['select'] == "all" or self.arguments['select'] == "*":
                self.tables_to_load = [TABLE_ENTRY_AGGREGATORS, TABLE_ENTRY_DATASET_MAPPINGS,
                                       TABLE_ENTRY_DATASET_RELATIONSHIPS, TABLE_ENTRY_ENTITY, TABLE_ENTRY_FILTERS,
                                       TABLE_ENTRY_ORDER, TABLE_ENTRY_PATH, TABLE_ENTRY_HAVING,
                                       TABLE_ENTRY_DV_ENTITY, TABLE_ENTRY_DV_MAPPINGS, TABLE_ENTRY_DV_PROPERTIES,
                                       TABLE_ENTRY_FILES]
            if self.arguments['select'].lower() == TABLE_ENTRY_DATASET_MAPPINGS.lower():
                self.tables_to_load = [TABLE_ENTRY_DATASET_MAPPINGS]
            if self.arguments['select'].lower() == TABLE_ENTRY_DATASET_RELATIONSHIPS.lower():
                self.tables_to_load = [TABLE_ENTRY_DATASET_RELATIONSHIPS]
            if self.arguments['select'].lower() == TABLE_ENTRY_ENTITY.lower():
                self.tables_to_load = [TABLE_ENTRY_ENTITY]
            if self.arguments['select'].lower() == TABLE_ENTRY_FILTERS.lower():
                self.tables_to_load = [TABLE_ENTRY_FILTERS]
            if self.arguments['select'].lower() == TABLE_ENTRY_ORDER.lower():
                self.tables_to_load = [TABLE_ENTRY_ORDER]
            if self.arguments['select'].lower() == TABLE_ENTRY_PATH.lower():
                self.tables_to_load = [TABLE_ENTRY_PATH]
            if self.arguments['select'].lower() == TABLE_ENTRY_HAVING.lower():
                self.tables_to_load = [TABLE_ENTRY_HAVING]
            if self.arguments['select'].lower() == TABLE_ENTRY_AGGREGATORS.lower():
                self.tables_to_load = [TABLE_ENTRY_AGGREGATORS]
            if self.arguments['select'].lower() == TABLE_ENTRY_DV_ENTITY.lower():
                self.tables_to_load = [TABLE_ENTRY_DV_ENTITY]
            if self.arguments['select'].lower() == TABLE_ENTRY_DV_MAPPINGS.lower():
                self.tables_to_load = [TABLE_ENTRY_DV_MAPPINGS]
            if self.arguments['select'].lower() == TABLE_ENTRY_DV_PROPERTIES.lower():
                self.tables_to_load = [TABLE_ENTRY_DV_PROPERTIES]
            if self.arguments['select'].lower() == TABLE_ENTRY_FILES.lower():
                self.tables_to_load = [TABLE_ENTRY_FILES]

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()

        self.log.log(self.engine_name, "Starting to commit metadata from owner ["+self.owner+"]", LOG_LEVEL_INFO)
        connection_type = self.configuration['metadata']['connection_type']
        self.connection = ConnectionFactory().get_connection(connection_type)
        self.connection.setup_connection(self.configuration['metadata'], self.log)

        self.delete_metadata_entry()
        self.copy_metadata_git()

        self.connection.commit()
        self.connection.close()

        super().finish_execution()


    def delete_metadata_entry(self):
        self.log.log(self.engine_name, "Starting to delete actual metadata", LOG_LEVEL_INFO)

        where_filter = COLUMN_ENTRY_OWNER+"='"+self.owner+"'"
        connection_type = self.configuration['metadata']['connection_type']

        # ENTRY_PATH
        if TABLE_ENTRY_PATH in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_PATH)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_ENTITY
        if TABLE_ENTRY_ENTITY in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_ENTITY)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_ORDER
        if TABLE_ENTRY_ORDER in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_ORDER)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_HAVING
        if TABLE_ENTRY_HAVING in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_HAVING)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_FILTERS
        if TABLE_ENTRY_FILTERS in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_FILTERS)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_DATASET_MAPPINGS
        if TABLE_ENTRY_DATASET_MAPPINGS in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_DATASET_MAPPINGS)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_DATASET_RELATIONSHIPS
        if TABLE_ENTRY_DATASET_RELATIONSHIPS in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_DATASET_RELATIONSHIPS)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_AGGREGATORS
        if TABLE_ENTRY_AGGREGATORS in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_AGGREGATORS)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_DV_ENTITY
        if TABLE_ENTRY_DV_ENTITY in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_DV_ENTITY)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_DV_MAPPINGS
        if TABLE_ENTRY_DV_MAPPINGS in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_DV_MAPPINGS)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_DV_PROPERTIES
        if TABLE_ENTRY_DV_PROPERTIES in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_DV_PROPERTIES)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        # ENTRY_FILES
        if TABLE_ENTRY_FILES in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_DELETE)
            query.set_target_table(TABLE_ENTRY_FILES)
            query.set_where_filters(where_filter)
            self.connection.execute(str(query))

        self.log.log(self.engine_name, "Finished to delete actual metadata", LOG_LEVEL_INFO)

    def copy_metadata_git(self):
        self.log.log(self.engine_name, "Starting to load backup metadata", LOG_LEVEL_INFO)
        where_filter = COLUMN_GIT_ENTRY_OWNER + "='" + self.owner + "'"
        connection_type = self.configuration['metadata']['connection_type']

        # GIT_ENTRY_PATH
        if TABLE_ENTRY_PATH in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_PATH)
            query.set_insert_columns(COLUMNS_ENTRY_PATH)
            query.set_select_columns(COLUMNS_GIT_ENTRY_PATH)
            query.set_from_tables([TABLE_GIT_ENTRY_PATH])
            self.connection.execute(str(query))

        # GIT_ENTRY_ENTITY
        if TABLE_ENTRY_ENTITY in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_ENTITY)
            query.set_insert_columns(COLUMNS_ENTRY_ENTITY)
            query.set_select_columns(COLUMNS_GIT_ENTRY_ENTITY)
            query.set_from_tables([TABLE_GIT_ENTRY_ENTITY])
            self.connection.execute(str(query))

        # GIT_ENTRY_ORDER
        if TABLE_ENTRY_ORDER in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_ORDER)
            query.set_insert_columns(COLUMNS_ENTRY_ORDER)
            query.set_select_columns(COLUMNS_GIT_ENTRY_ORDER)
            query.set_from_tables([TABLE_GIT_ENTRY_ORDER])
            self.connection.execute(str(query))

        # GIT_ENTRY_HAVING
        if TABLE_ENTRY_HAVING in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_HAVING)
            query.set_insert_columns(COLUMNS_ENTRY_HAVING)
            query.set_select_columns(COLUMNS_GIT_ENTRY_HAVING)
            query.set_from_tables([TABLE_GIT_ENTRY_HAVING])
            self.connection.execute(str(query))

        # GIT_ENTRY_FILTERS
        if TABLE_ENTRY_FILTERS in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_FILTERS)
            query.set_insert_columns(COLUMNS_ENTRY_FILTERS)
            query.set_select_columns(COLUMNS_GIT_ENTRY_FILTERS)
            query.set_from_tables([TABLE_GIT_ENTRY_FILTERS])
            self.connection.execute(str(query))

        # GIT_ENTRY_DATASET_MAPPINGS
        if TABLE_ENTRY_DATASET_MAPPINGS in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_DATASET_MAPPINGS)
            query.set_insert_columns(COLUMNS_ENTRY_DATASET_MAPPINGS)
            query.set_select_columns(COLUMNS_GIT_ENTRY_DATASET_MAPPINGS)
            query.set_from_tables([TABLE_GIT_ENTRY_DATASET_MAPPINGS])
            self.connection.execute(str(query))

        # GIT_ENTRY_DATASET_RELATIONSHIPS
        if TABLE_ENTRY_DATASET_RELATIONSHIPS in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_DATASET_RELATIONSHIPS)
            query.set_insert_columns(COLUMNS_ENTRY_DATASET_RELATIONSHIPS)
            query.set_select_columns(COLUMNS_GIT_ENTRY_DATASET_RELATIONSHIPS)
            query.set_from_tables([TABLE_GIT_ENTRY_DATASET_RELATIONSHIPS])
            self.connection.execute(str(query))

        # GIT_ENTRY_AGGREGATORS
        if TABLE_ENTRY_AGGREGATORS in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_AGGREGATORS)
            query.set_insert_columns(COLUMNS_ENTRY_AGGREGATORS)
            query.set_select_columns(COLUMNS_GIT_ENTRY_AGGREGATORS)
            query.set_from_tables([TABLE_GIT_ENTRY_AGGREGATORS])
            self.connection.execute(str(query))

        # GIT_ENTRY_DV_ENTITY
        if TABLE_ENTRY_DV_ENTITY in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_DV_ENTITY)
            query.set_insert_columns(COLUMNS_ENTRY_DV_ENTITY)
            query.set_select_columns(COLUMNS_GIT_ENTRY_DV_ENTITY)
            query.set_from_tables([TABLE_GIT_ENTRY_DV_ENTITY])
            self.connection.execute(str(query))

        # GIT_ENTRY_DV_MAPPINGS
        if TABLE_ENTRY_DV_MAPPINGS in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_DV_MAPPINGS)
            query.set_insert_columns(COLUMNS_ENTRY_DV_MAPPINGS)
            query.set_select_columns(COLUMNS_GIT_ENTRY_DV_MAPPINGS)
            query.set_from_tables([TABLE_GIT_ENTRY_DV_MAPPINGS])
            self.connection.execute(str(query))

        # GIT_ENTRY_DV_PROPERTIES
        if TABLE_ENTRY_DV_PROPERTIES in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_DV_PROPERTIES)
            query.set_insert_columns(COLUMNS_ENTRY_DV_PROPERTIES)
            query.set_select_columns(COLUMNS_GIT_ENTRY_DV_PROPERTIES)
            query.set_from_tables([TABLE_GIT_ENTRY_DV_PROPERTIES])
            self.connection.execute(str(query))

        # GIT_ENTRY_DV_PROPERTIES
        if TABLE_ENTRY_FILES in self.tables_to_load:
            query = Query()
            query.set_database(connection_type)
            query.set_type(QUERY_TYPE_INSERT)
            query.set_where_filters(where_filter)
            query.set_target_table(TABLE_ENTRY_FILES)
            query.set_insert_columns(COLUMNS_ENTRY_FILES)
            query.set_select_columns(COLUMNS_GIT_ENTRY_FILES)
            query.set_from_tables([TABLE_GIT_ENTRY_FILES])
            self.connection.execute(str(query))

        self.log.log(self.engine_name, "Finished to load backup metadata", LOG_LEVEL_INFO)