from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.query import Query

class EngineCommit(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Commit"
        self.engine_command = "commit"

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()

        self.log.log(self.engine_name, "Starting to commit metadata from owner ["+self.owner+"]", LOG_LEVEL_INFO)
        connection_type = self.configuration['metadata']['connection_type']
        self.connection = ConnectionFactory().get_connection(connection_type)
        self.connection.setup_connection(self.configuration['metadata'], self.log)

        self.delete_metadata_git()
        self.copy_metadata_git()

        self.connection.commit()
        self.connection.close()

        super().finish_execution()


    def delete_metadata_git(self):
        self.log.log(self.engine_name, "Starting to delete previous metadata version", LOG_LEVEL_INFO)

        where_filter = COLUMN_GIT_ENTRY_OWNER+"='"+self.owner+"'"
        connection_type = (self.configuration['metadata']['connection_type']).upper()

        # GIT_ENTRY_PATH
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_PATH)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_ENTITY
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_ENTITY)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_ORDER
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_ORDER)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_HAVING
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_HAVING)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_FILTERS
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_FILTERS)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_DATASET_MAPPINGS
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_DATASET_MAPPINGS)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_DATASET_RELATIONSHIPS
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_DATASET_RELATIONSHIPS)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_AGGREGATORS
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_AGGREGATORS)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_DV_ENTITY
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_DV_ENTITY)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_DV_MAPPINGS
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_DV_MAPPINGS)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_DV_PROPERTIES
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_DV_PROPERTIES)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # GIT_ENTRY_DV_PROPERTIES
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_GIT_ENTRY_FILES)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        self.log.log(self.engine_name, "Finished to delete previous metadata version", LOG_LEVEL_INFO)

    def copy_metadata_git(self):
        self.log.log(self.engine_name, "Starting to load active metadata version", LOG_LEVEL_INFO)
        where_filter = COLUMN_ENTRY_OWNER + "='" + self.owner + "'"
        connection_type = (self.configuration['metadata']['connection_type']).upper()

        # GIT_ENTRY_PATH
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_PATH)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_PATH)
        query.set_select_columns(COLUMNS_ENTRY_PATH)
        query.set_from_tables([TABLE_ENTRY_PATH])
        self.connection.execute(str(query))

        # GIT_ENTRY_ENTITY
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_ENTITY)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_ENTITY)
        query.set_select_columns(COLUMNS_ENTRY_ENTITY)
        query.set_from_tables([TABLE_ENTRY_ENTITY])
        self.connection.execute(str(query))

        # GIT_ENTRY_ORDER
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_ORDER)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_ORDER)
        query.set_select_columns(COLUMNS_ENTRY_ORDER)
        query.set_from_tables([TABLE_ENTRY_ORDER])
        self.connection.execute(str(query))

        # GIT_ENTRY_HAVING
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_HAVING)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_HAVING)
        query.set_select_columns(COLUMNS_ENTRY_HAVING)
        query.set_from_tables([TABLE_ENTRY_HAVING])
        self.connection.execute(str(query))

        # GIT_ENTRY_FILTERS
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_FILTERS)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_FILTERS)
        query.set_select_columns(COLUMNS_ENTRY_FILTERS)
        query.set_from_tables([TABLE_ENTRY_FILTERS])
        self.connection.execute(str(query))

        # GIT_ENTRY_DATASET_MAPPINGS
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_DATASET_MAPPINGS)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_DATASET_MAPPINGS)
        query.set_select_columns(COLUMNS_ENTRY_DATASET_MAPPINGS)
        query.set_from_tables([TABLE_ENTRY_DATASET_MAPPINGS])
        self.connection.execute(str(query))

        # GIT_ENTRY_DATASET_RELATIONSHIPS
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_DATASET_RELATIONSHIPS)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_DATASET_RELATIONSHIPS)
        query.set_select_columns(COLUMNS_ENTRY_DATASET_RELATIONSHIPS)
        query.set_from_tables([TABLE_ENTRY_DATASET_RELATIONSHIPS])
        self.connection.execute(str(query))

        # GIT_ENTRY_AGGREGATORS
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_AGGREGATORS)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_AGGREGATORS)
        query.set_select_columns(COLUMNS_ENTRY_AGGREGATORS)
        query.set_from_tables([TABLE_ENTRY_AGGREGATORS])
        self.connection.execute(str(query))

        # GIT_ENTRY_DV_ENTITY
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_DV_ENTITY)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_DV_ENTITY)
        query.set_select_columns(COLUMNS_ENTRY_DV_ENTITY)
        query.set_from_tables([TABLE_ENTRY_DV_ENTITY])
        self.connection.execute(str(query))

        # GIT_ENTRY_DV_MAPPINGS
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_DV_MAPPINGS)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_DV_MAPPINGS)
        query.set_select_columns(COLUMNS_ENTRY_DV_MAPPINGS)
        query.set_from_tables([TABLE_ENTRY_DV_MAPPINGS])
        self.connection.execute(str(query))

        # GIT_ENTRY_DV_PROPERTIES
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_DV_PROPERTIES)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_DV_PROPERTIES)
        query.set_select_columns(COLUMNS_ENTRY_DV_PROPERTIES)
        query.set_from_tables([TABLE_ENTRY_DV_PROPERTIES])
        self.connection.execute(str(query))

        # GIT_ENTRY_DV_PROPERTIES
        query = Query()
        query.set_type(QUERY_TYPE_INSERT)
        query.set_database(connection_type)
        query.set_where_filters(where_filter)
        query.set_target_table(TABLE_GIT_ENTRY_FILES)
        query.set_insert_columns(COLUMNS_GIT_ENTRY_FILES)
        query.set_select_columns(COLUMNS_ENTRY_FILES)
        query.set_from_tables([TABLE_ENTRY_FILES])
        self.connection.execute(str(query))


        self.log.log(self.engine_name, "Finished to load active metadata version", LOG_LEVEL_INFO)