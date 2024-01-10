from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.constants import *
import yaml
import os

class EngineInit(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Init"
        self.engine_command = "init"
        self.database_default = CONNECTION_SQLITE.lower()

        self.metadata_database = None
        self.data_database = None
        if 'metadata' in self.arguments:
            self.metadata_database = self.arguments['metadata']
        if 'database' in self.arguments:
            self.data_database = self.arguments['database']
        if self.metadata_database is not None and self.data_database is not None:
            self.log.log(self.engine_name,
                         "The configuration file is going to be created for the data database [" + self.data_database + "] and metadata database ["+ self.metadata_database + "]",
                         LOG_LEVEL_INFO)
        if self.metadata_database is None and self.data_database is None:
            self.metadata_database = self.database_default
            self.data_database = self.database_default
            self.log.log(self.engine_name, "The configuration file is going to be created for the default database [" + self.database_default + "]", LOG_LEVEL_INFO)
        if self.metadata_database is None and self.data_database is not None:
            self.metadata_database = self.data_database
            self.log.log(self.engine_name,
                         "The configuration file is going to be created for the Data Database selected [" + self.data_database + "]",
                         LOG_LEVEL_INFO)
        if self.data_database is None and self.metadata_database is not None:
            self.log.log(self.engine_name,
                         "The configuration file is going to be created for the Metadata Database selected [" + self.metadata_database + "]",
                         LOG_LEVEL_INFO)
            self.data_database = self.metadata_database

    def run(self):
        super().start_execution(need_configuration_file=False, need_connection_validation=False)

        # Create Configuration File
        file_controller_configuration = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
        file_controller_configuration.set_file_location(ACTUAL_PATH, CONFIGURATION_FILE_NAME)
        file_controller_configuration.setup_writer(FILE_WRITER_NEW_FILE)

        # Read Template OUTPUT & MODULES
        file_controller_configuration_template = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
        file_controller_configuration_template.set_file_location(os.path.join(PACKAGE_PATH, CONFIGURATION_FILE_PATH), CONFIGURATION_FILE_NAME)
        self.configuration_file = file_controller_configuration_template.read_file()
        file_controller_configuration.write_file(self.configuration_file)

        # Read Template DATA
        file_controller_configuration_template = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
        file_controller_configuration_template.set_file_location(os.path.join(PACKAGE_PATH, CONFIGURATION_FILE_PATH, self.data_database.lower()), CONFIGURATION_FILE_DATA + self.data_database + "." + FILE_TYPE_YML)
        self.configuration_file = file_controller_configuration_template.read_file()
        file_controller_configuration.write_file(self.configuration_file)

        # Read Template METADATA
        file_controller_configuration_template = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
        file_controller_configuration_template.set_file_location(os.path.join(PACKAGE_PATH, CONFIGURATION_FILE_PATH, self.metadata_database.lower()), CONFIGURATION_FILE_METADATA + self.metadata_database + "." + FILE_TYPE_YML)
        self.configuration_file = file_controller_configuration_template.read_file()
        file_controller_configuration.write_file(self.configuration_file)

        # Create folder
        if not os.path.exists(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH)):
            os.mkdir(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH))
        if not os.path.exists(os.path.join(ACTUAL_PATH, OUTPUT_FILES_PATH)):
            os.mkdir(os.path.join(ACTUAL_PATH, OUTPUT_FILES_PATH))
        if not os.path.exists(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH)):
            os.mkdir(os.path.join(ACTUAL_PATH, BACKUP_FILES_PATH))

        # Create files - Metadata Entry
        all_entry_files = os.listdir(os.path.join(PACKAGE_PATH, ENTRY_FILES_PATH))
        for file in all_entry_files:
            file_controller = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller.set_file_location(os.path.join(PACKAGE_PATH, ENTRY_FILES_PATH), file)
            file_to_write = file_controller.read_file()

            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), file)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(file_to_write)

        super().finish_execution()