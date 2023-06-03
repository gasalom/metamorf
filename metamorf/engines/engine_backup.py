from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *

class EngineBackup(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Backup"
        self.engine_command = "backup"

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()

        self.metadata_actual = self.load_metadata(load_om=True, load_entry=False, load_ref=True, load_im=False, owner=self.owner)

        self.log.log(self.engine_name, "Start to backup the system for the owner ["+self.owner + "]", LOG_LEVEL_INFO)
        # OM_DATASET
        content = []
        content.append(COLUMNS_OM_DATASET)
        for registry in self.metadata_actual.om_dataset: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_DV
        content = []
        content.append(COLUMNS_OM_DATASET_DV)
        for registry in self.metadata_actual.om_dataset_dv: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_DV)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_T_ORDER
        content = []
        content.append(COLUMNS_OM_DATASET_T_ORDER)
        for registry in self.metadata_actual.om_dataset_t_order: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_T_ORDER)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_SPECIFICATION
        content = []
        content.append(COLUMNS_OM_DATASET_SPECIFICATION)
        for registry in self.metadata_actual.om_dataset_specification: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_SPECIFICATION)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_T_MAPPING
        content = []
        content.append(COLUMNS_OM_DATASET_T_MAPPING)
        for registry in self.metadata_actual.om_dataset_t_mapping: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_T_MAPPING)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_T_HAVING
        content = []
        content.append(COLUMNS_OM_DATASET_T_HAVING)
        for registry in self.metadata_actual.om_dataset_t_having: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_T_HAVING)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_T_AGG
        content = []
        content.append(COLUMNS_OM_DATASET_T_AGG)
        for registry in self.metadata_actual.om_dataset_t_agg: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_T_AGG)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_T_FILTER
        content = []
        content.append(COLUMNS_OM_DATASET_T_FILTER)
        for registry in self.metadata_actual.om_dataset_t_filter: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_T_FILTER)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_RELATIONSHIPS
        content = []
        content.append(COLUMNS_OM_DATASET_RELATIONSHIPS)
        for registry in self.metadata_actual.om_dataset_relationships: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_RELATIONSHIPS)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_EXECUTION
        content = []
        content.append(COLUMNS_OM_DATASET_EXECUTION)
        for registry in self.metadata_actual.om_dataset_execution: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_EXECUTION)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_PATH
        content = []
        content.append(COLUMNS_OM_DATASET_PATH)
        for registry in self.metadata_actual.om_dataset_path: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_PATH)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_DATASET_T_DISTINCT
        content = []
        content.append(COLUMNS_OM_DATASET_T_DISTINCT)
        for registry in self.metadata_actual.om_dataset_t_distinct: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_DATASET_T_DISTINCT)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        # OM_PROPERTIES
        content = []
        content.append(COLUMNS_OM_PROPERTIES)
        for registry in self.metadata_actual.om_properties: content.append(registry.get())
        file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
        file_controller_final.set_file_location(os.path.join(ACTUAL_PATH , BACKUP_FILES_PATH), TABLE_OM_PROPERTIES)
        file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
        file_controller_final.write_file(content)
        file_controller_final.close()

        self.log.log(self.engine_name, "Finish to backup the system for the owner [" + self.owner + "]", LOG_LEVEL_INFO)

        super().finish_execution()