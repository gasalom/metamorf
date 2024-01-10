from metamorf.engines.engine import Engine
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.metadata_validator import MetadataValidator

class EngineMetadata(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Metadata"
        self.engine_command = "metadata"

    def run(self):
        super().start_execution()

        self.connection = ConnectionFactory().get_connection(self.configuration['data']['connection_type'])
        self.connection_metadata = ConnectionFactory().get_connection(self.configuration['metadata']['connection_type'])
        self.metadata_actual = self.load_metadata(load_om=True, load_entry=True, load_ref=True, load_im=False, owner=self.owner)

        # If there's nothing to load it finishes the execution
        if len(self.metadata_actual.entry_entity) == 0:
            self.log.log(self.engine_name, "There is nothing to validate.", LOG_LEVEL_WARNING)
            super().finish_execution(True)
            return

        metadata_validator = MetadataValidator(self.metadata_actual, self.connection, self.configuration, self.log)
        result_validation_metadata_entry = metadata_validator.validate_metadata()
        if result_validation_metadata_entry == False:
            self.log.log(self.engine_name, "Metadata Entry Validation has not passed. Please review the errors.", LOG_LEVEL_CRITICAL)
            super().finish_execution(False)
            return
        else:
            self.log.log(self.engine_name, "Metadata Entry validation - Ok", LOG_LEVEL_OK)

        super().finish_execution()