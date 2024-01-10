from abc import ABC, abstractmethod
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.configvalidator import ConfigValidator
from metamorf.constants import *
import sys
from metamorf.tools.log import Log
from metamorf.tools.connection import ConnectionFactory
from metamorf.tools.utils import get_metadata_from_database

class Engine(ABC):

    def __init__(self, log: Log, arguments: dict):
        self.log = log
        self.arguments = arguments
        self.configuration_file_loaded = False
        self.configuration_file = None
        self.properties_file = None
        self.owner = None
        self.metadata = None
        self.engine_name = 'ENGINE METAMORF'
        self.engine_command = 'ENGINE COMMAND'
        self._initialize_engine()
        self.log.log(self.engine_name, 'Initiating engine', LOG_LEVEL_INFO)
        self.log.log(self.engine_name, 'Loaded the arguments: ' + str(arguments), LOG_LEVEL_ONLY_LOG)
        self.configuration = dict()

    def _initialize_configuration(self):
        self.configuration['name'] = self.configuration_file['name']
        self.configuration['owner'] = self.configuration_file['owner']

        self.configuration['modules'] = dict()

        self.configuration['modules']['elt'] = dict()
        self.configuration['modules']['elt']['threads'] = 1
        self.configuration['modules']['elt']['execution'] = 'run'
        self.configuration['modules']['elt']['on_schema_change'] = 'ignore'
        self.configuration['modules']['elt']['create_database'] = False
        self.configuration['modules']['elt']['create_schema'] = False

        self.configuration['modules']['datavault'] = dict()
        self.configuration['modules']['datavault']['char_separator_naming'] = '_'
        self.configuration['modules']['datavault']['hash'] = CONFIG_HASH_DV_MD5

        self.configuration['output'] = dict()
        self.configuration['output']['type'] = 'sql'

        self.configuration['api'] = dict()
        self.configuration['api']['port'] = 5555
        self.configuration['api']['host'] = 'localhost'

        self.configuration['data'] = self.configuration_file['data']
        self.configuration['metadata'] = self.configuration_file['metadata']

        self.configuration['active_modules'] = []
        self.configuration['active_modules'].append(MODULE_ELT)


    def _initialize_config_modules(self):
        if 'modules' in self.configuration_file:
            for m in self.configuration_file['modules']:
                if m['name'] == "elt":
                    if 'threads' in m:
                        self.configuration['modules']['elt']['threads'] = m['threads']
                    if 'execution' in m:
                        self.configuration['modules']['elt']['execution'] = m['execution']
                    if 'on_schema_change' in m:
                        self.configuration['modules']['elt']['on_schema_change'] = m['on_schema_change']
                    if 'create_database' in m:
                        self.configuration['modules']['elt']['create_database'] = m['create_database']
                    if 'create_schema' in m:
                        self.configuration['modules']['elt']['create_schema'] = m['create_schema']
                if m['name'] == "datavault":
                    self.configuration['active_modules'].append(MODULE_DV)
                    if 'char_separator_naming' in m:
                        self.configuration['modules']['datavault']['char_separator_naming'] = m['char_separator_naming']
                    if 'hash' in m:
                        self.configuration['modules']['datavault']['hash'] = m['hash']

    def _initialize_config_api(self):
        if 'api' not in self.configuration_file:
            self.configuration['api']['port'] = self.properties_file['api']['port']
            self.configuration['api']['host'] = self.properties_file['api']['host']
        else:
            if 'port' not in self.configuration_file['api']:
                self.configuration['api']['port'] = self.properties_file['api']['port']
            else:
                self.configuration['api']['port'] = self.configuration_file['api']['port']
            if 'host' not in self.configuration_file['api']:
                self.configuration['api']['host'] = self.properties_file['api']['host']
            else:
                self.configuration['api']['host'] = self.configuration_file['api']['host']

    def _load_configuration_files(self):
        """Gets the Configuration and Properties File and validates it. Returns the result. """
        self.log.log(self.engine_name, 'Starting configuration file validation', LOG_LEVEL_INFO)

        # Configuration File
        file_controller_configuration = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
        file_controller_configuration.set_file_location(ACTUAL_PATH, CONFIGURATION_FILE_NAME)
        self.configuration_file = file_controller_configuration.read_file()
        if self.configuration_file is not None:
            self.configuration_file_loaded = True

        # Properties File
        file_controller_properties = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
        file_controller_properties.set_file_location(os.path.join(PACKAGE_PATH , PROPERTIES_FILE_PATH), PROPERTIES_FILE_NAME)
        self.properties_file = file_controller_properties.read_file()

        # Properties and Configuration File
        configuration_validator = ConfigValidator(self.properties_file,self.configuration_file, self.log)
        result_configuration = configuration_validator.validate()
        if result_configuration: self.log.log(self.engine_name, 'Finished configuration file validation - Ok', LOG_LEVEL_OK)
        if not result_configuration: self.log.log(self.engine_name, 'Finished configuration file validation - Not Ok', LOG_LEVEL_ERROR)
        if not self.configuration_file_loaded:
            self.log.log(self.engine_name, 'Configuration file not exists at "'+ ACTUAL_PATH + '"', LOG_LEVEL_ERROR)

        if self.configuration_file_loaded and result_configuration:
            self._initialize_configuration()
            self._initialize_config_modules()
            self._initialize_config_api()

        return result_configuration

    def _test_connections_to_databases(self):
        connection_type = self.configuration['metadata']['connection_type']
        connection_metadata = ConnectionFactory().get_connection(connection_type)
        result = connection_metadata.setup_connection(self.configuration['metadata'], self.log)

        connection_type = self.configuration['data']['connection_type']
        connection_data = ConnectionFactory().get_connection(connection_type)
        result = result and connection_data.setup_connection(self.configuration['data'], self.log)

        if result:
            metadata_schemas = connection_metadata.get_schemas_available()
            if connection_metadata.schema not in metadata_schemas:
                result = False
                self.log.log(self.engine_name, 'Can not connect to the schema indicated on Metadata Connection', LOG_LEVEL_ERROR)
            data_schemas = connection_data.get_schemas_available()
            if connection_data.schema not in data_schemas:
                result = False
                self.log.log(self.engine_name, 'Can not connect to the schema indicated on Data Connection', LOG_LEVEL_ERROR)

        return result

    @abstractmethod
    def run(self):
        """Execution of the engine."""
        pass

    @abstractmethod
    def _initialize_engine(self):
        """Need to be implemented defining self.engine_name and self.engine_command. Called on the __init__."""
        pass

    def _need_configuration_file_error(self):
        """Throw error message for configuration file."""
        self.log.log(self.engine_name, 'The engine can not execute without a configuration file. Try to generate it with "INIT" command.', LOG_LEVEL_ERROR)

    def start_execution(self, need_configuration_file: bool=True, need_connection_validation: bool=True):
        """Method called at start of engine run() execution. Loads the ConfigurationFile if need_configuration_file is set on True.
        If the validation doesn't pass it finishes the execution."""

        self.log.log(self.engine_name, 'Starting execution, command [' + self.engine_command + '] initiating', LOG_LEVEL_INFO)
        if need_configuration_file:
            if not self._load_configuration_files():
                if self.configuration_file_loaded is False:
                    self._need_configuration_file_error()
                self.log.log(self.engine_name, 'Execution finished with errors.', LOG_LEVEL_ERROR)
                sys.exit()
            self.owner = self.configuration['owner']
            self.log.log(self.engine_name, 'Using profile [' + self.owner + "]", LOG_LEVEL_INFO)
        if need_connection_validation:
            if not self._test_connections_to_databases():
                self.log.log(self.engine_name, 'Execution finished with errors.', LOG_LEVEL_ERROR)
                sys.exit()

    def finish_execution(self, result: bool = True):
        """Method called at end of engine run() execution. Inserts on the log."""
        if result:
            self.log.log(self.engine_name, 'Execution finished Ok', LOG_LEVEL_OK)
        else:
            self.log.log(self.engine_name, 'Execution finished with errors', LOG_LEVEL_ERROR)
        self.log.close()
        sys.exit()

    def load_metadata(self, load_om: bool=True, load_ref: bool=True, load_entry: bool=True, load_im: bool=True, owner: str=None):
        """Loads the attribute self.metadata from the engine, if fails Metamorf finishes."""
        # Get connection to the Metadata Database
        connection_type = self.configuration['metadata']['connection_type']
        connection = ConnectionFactory().get_connection(connection_type)
        connection.setup_connection(self.configuration['metadata'], self.log)
        if owner is None: owner = self.owner

        # Load Metadata
        metadata = get_metadata_from_database(connection, self.log, owner, load_om, load_ref, load_entry, load_im)
        connection.close()
        if metadata is None:
            self.finish_execution(False)
        return metadata
