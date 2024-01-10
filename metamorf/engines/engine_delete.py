from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.query import Query

class EngineDelete(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Delete"
        self.engine_command = "delete"

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()

        self.log.log(self.engine_name, "Starting to delete metadata from owner ["+self.owner+"]", LOG_LEVEL_INFO)
        connection_type = self.configuration['metadata']['connection_type']
        self.connection = ConnectionFactory().get_connection(connection_type)
        self.connection.setup_connection(self.configuration['metadata'], self.log)

        self.delete_metadata_entry()

        self.connection.commit()
        self.connection.close()

        super().finish_execution()

    def delete_metadata_entry(self):
        self.log.log(self.engine_name, "Starting to delete actual metadata", LOG_LEVEL_INFO)

        where_filter = COLUMN_ENTRY_OWNER+"='"+self.owner+"'"
        connection_type = self.configuration['metadata']['connection_type']

        # ENTRY_PATH
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_PATH)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_ENTITY
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_ENTITY)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_ORDER
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_ORDER)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_HAVING
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_HAVING)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_FILTERS
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_FILTERS)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_DATASET_MAPPINGS
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_DATASET_MAPPINGS)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_DATASET_RELATIONSHIPS
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_DATASET_RELATIONSHIPS)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_AGGREGATORS
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_AGGREGATORS)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_FILES
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_FILES)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_DV_MAPPINGS
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_DV_MAPPINGS)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_DV_ENTITY
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_DV_ENTITY)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        # ENTRY_DV_PROPERTIES
        query = Query()
        query.set_database(connection_type)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_ENTRY_DV_PROPERTIES)
        query.set_where_filters(where_filter)
        self.connection.execute(str(query))

        self.log.log(self.engine_name, "Finished to delete actual metadata", LOG_LEVEL_INFO)
