from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *

class EngineValidate(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Validate"
        self.engine_command = "validate"

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()

        self.log.log(self.engine_name, "Starting to validate metadata connection", LOG_LEVEL_INFO)
        connection_type = self.configuration_file['metadata']['connection_type']
        connection = ConnectionFactory().get_connection(connection_type)
        connection.setup_connection(self.configuration_file['metadata'], self.log)
        self.log.log(self.engine_name, "Metadata connection validation finished", LOG_LEVEL_INFO)

        self.log.log(self.engine_name, "Starting to validate data connection", LOG_LEVEL_INFO)
        connection_type = self.configuration_file['data']['connection_type']
        connection = ConnectionFactory().get_connection(connection_type)
        connection.setup_connection(self.configuration_file['data'], self.log)
        self.log.log(self.engine_name, "Data connection validation finished", LOG_LEVEL_INFO)


        super().finish_execution()