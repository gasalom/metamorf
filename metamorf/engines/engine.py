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
        self.modules_to_execute = []

    def _initialize_config_modules(self):
        if 'modules' in self.configuration_file:
            for m in self.configuration_file['modules']:
                if m['name'] == "elt":
                    if 'status' in m:
                        if m['status'] == 'ACTIVE':
                            self.modules_to_execute.append(MODULE_ELT)
                    else:
                        m['status'] = "INACTIVE"
                if m['name'] == "datavault":
                    if 'status' in m:
                        if m['status'] == "ACTIVE":
                            self.modules_to_execute.append(MODULE_DV)
                    else:
                        m['status'] = 'INACTIVE'
                    if 'char_separator_naming' in m:
                        self.module_dv_char_separator_naming = m['char_separator_naming']
                    else:
                        m['char_separator_naming'] = '_'

    def _initialize_config_api(self):
        if 'api' not in self.configuration_file:
            api_properties = dict()
            api_properties['port'] = self.properties_file['api']['port']
            api_properties['host'] = self.properties_file['api']['host']
            self.configuration_file['api'] = api_properties
        else:
            if 'port' not in self.configuration_file['api']:
                self.configuration_file['api']['port'] = self.properties_file['api']['port']
            if 'host' not in self.configuration_file['api']:
                self.configuration_file['api']['host'] = self.properties_file['api']['host']



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

        if self.configuration_file_loaded:
            self._initialize_config_modules()
            self._initialize_config_api()

        return result_configuration

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

    def start_execution(self, need_configuration_file: bool=True):
        """Method called at start of engine run() execution. Loads the ConfigurationFile if need_configuration_file is set on True.
        If the validation doesn't pass it finishes the execution."""

        self.log.log(self.engine_name, 'Starting execution, command [' + self.engine_command + '] initiating', LOG_LEVEL_INFO)
        if need_configuration_file:
            if not self._load_configuration_files():
                if self.configuration_file_loaded is False:
                    self._need_configuration_file_error()
                self.log.log(self.engine_name, 'Execution finished with errors.', LOG_LEVEL_ERROR)
                sys.exit()
            self.owner = self.configuration_file['owner']
            self.log.log(self.engine_name, 'Using profile [' + self.owner + "]", LOG_LEVEL_INFO)

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
        connection_type = self.configuration_file['metadata']['connection_type']
        connection = ConnectionFactory().get_connection(connection_type)
        connection.setup_connection(self.configuration_file['metadata'], self.log)
        if owner is None: owner = self.owner

        # Load Metadata
        metadata = get_metadata_from_database(connection, self.log, owner, load_om, load_ref, load_entry, load_im)
        connection.close()
        if metadata is None:
            self.finish_execution(False)
        return metadata
