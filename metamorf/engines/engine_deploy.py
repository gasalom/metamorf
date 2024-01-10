from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
import os

class EngineDeploy(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Deploy"
        self.engine_command = "deploy"


    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution(need_connection_validation=False)

        # ARCHITECTURE INSTALATION
        connection_type = self.configuration['metadata']['connection_type']
        # Get File that will be executed
        file_controller_init_sql = FileControllerFactory().get_file_reader(FILE_TYPE_SQL)
        file_controller_init_sql.set_file_location(os.path.join(PACKAGE_PATH , INITIALIZATION_FILE_PATH , connection_type.lower()), "pre_init_" + connection_type.lower() + ".sql")
        file_init_sql = file_controller_init_sql.read_file()

        # Get Connection and Execute the Initialization
        self.log.log(self.engine_name, "Deploying Metamorf Architecture on the Metadata Database", LOG_LEVEL_INFO)
        connection = ConnectionFactory().get_connection(connection_type)
        connection.setup_connection(self.configuration['metadata'], self.log)
        connection.execute(file_init_sql)
        connection.commit()
        connection.close()

        # METAMORF INSTALATION
        connection_type = self.configuration['metadata']['connection_type']
        # Get File that will be executed
        file_controller_init_sql = FileControllerFactory().get_file_reader(FILE_TYPE_SQL)
        file_controller_init_sql.set_file_location(os.path.join(PACKAGE_PATH, INITIALIZATION_FILE_PATH, connection_type.lower()), "init_" + connection_type.lower() + ".sql")
        file_init_sql = file_controller_init_sql.read_file()

        # Get Connection and Execute the Initialization
        self.log.log(self.engine_name, "Deploying Metamorf on the Database indicated on Configuration File", LOG_LEVEL_INFO)
        connection = ConnectionFactory().get_connection(connection_type)
        connection.setup_connection(self.configuration['metadata'], self.log)
        connection.execute(file_init_sql)
        connection.commit()
        connection.close()
        super().finish_execution()


