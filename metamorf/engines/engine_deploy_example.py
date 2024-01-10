from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
import os

class EngineDeployExample(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Deploy Example"
        self.engine_command = "deploy-example"


    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution(need_connection_validation=False)

        # METADATA DEPLOYMENT EXAMPLE
        connection_type = self.configuration['metadata']['connection_type']
        connection_type_data = self.configuration['data']['connection_type']
        # Get File that will be executed
        file_controller_init_sql = FileControllerFactory().get_file_reader(FILE_TYPE_SQL)
        file_controller_init_sql.set_file_location(os.path.join(PACKAGE_PATH, INITIALIZATION_FILE_PATH, connection_type.lower()), "init_example_metadata_" + connection_type_data.lower() + ".sql")
        file_init_sql = file_controller_init_sql.read_file()

        # Get Connection and Execute the Deployment
        self.log.log(self.engine_name, "Deploying Metamorf Metadata Example on the Database indicated on Configuration File", LOG_LEVEL_INFO)
        connection = ConnectionFactory().get_connection(connection_type)
        connection.setup_connection(self.configuration['metadata'], self.log)
        result = connection.execute(file_init_sql)
        if not result:
            self.log.log(self.engine_name, "The deployment can't be performed. Make sure Metamorf is installed correctly. You can do it using [deploy] command.", LOG_LEVEL_ERROR)
            super().finish_execution(False)
        connection.commit()
        self.log.log(self.engine_name, "Deployment Metamorf Metadata Example Finished", LOG_LEVEL_INFO)
        connection.close()

        # DATA DEPLOYMENT EXAMPLE
        connection_type = self.configuration['data']['connection_type']
        # Get File that will be executed
        file_controller_init_sql = FileControllerFactory().get_file_reader(FILE_TYPE_SQL)
        file_controller_init_sql.set_file_location(os.path.join(PACKAGE_PATH, INITIALIZATION_FILE_PATH, connection_type.lower()), "init_example_data_" + connection_type.lower() + ".sql")
        file_init_sql = file_controller_init_sql.read_file()

        # Get Connection and Execute the Deployment
        self.log.log(self.engine_name, "Deploying Metamorf Data Example on the Database indicated on Configuration File", LOG_LEVEL_INFO)
        connection = ConnectionFactory().get_connection(connection_type)
        connection.setup_connection(self.configuration['data'], self.log)
        result = connection.execute(file_init_sql)
        if not result: super().finish_execution(False)
        connection.commit()
        self.log.log(self.engine_name, "Deploying Metamorf Data Example Finished", LOG_LEVEL_INFO)
        connection.close()

        super().finish_execution()



