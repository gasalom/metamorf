from metamorf.engines.engine import Engine
from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
import os

class EngineDownload(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Download"
        self.engine_command = "download"

    def _initialize_download_engine(self):
        # Default it will download all the files of the main owner
        self.entry_files_to_download = [FILE_ENTRY_AGGREGATORS, FILE_ENTRY_DATASET_MAPPINGS,
                                        FILE_ENTRY_DATASET_RELATIONSHIPS, FILE_ENTRY_ENTITY, FILE_ENTRY_FILTERS,
                                        FILE_ENTRY_ORDER, FILE_ENTRY_PATH, FILE_ENTRY_HAVING,
                                        FILE_ENTRY_DV_ENTITY, FILE_ENTRY_DV_MAPPINGS,FILE_ENTRY_DV_PROPERTIES,
                                        FILE_ENTRY_FILES]
        self.owner_to_download = self.owner

        if 'select' in self.arguments:
            if self.arguments['select'] == "all" or self.arguments['select'] == "*":
                self.entry_files_to_download = [FILE_ENTRY_AGGREGATORS, FILE_ENTRY_DATASET_MAPPINGS,
                                                FILE_ENTRY_DATASET_RELATIONSHIPS, FILE_ENTRY_ENTITY, FILE_ENTRY_FILTERS,
                                                FILE_ENTRY_ORDER, FILE_ENTRY_PATH, FILE_ENTRY_HAVING,
                                                FILE_ENTRY_DV_ENTITY, FILE_ENTRY_DV_MAPPINGS, FILE_ENTRY_DV_PROPERTIES,
                                                FILE_ENTRY_FILES]
            if self.arguments['select'].lower() == FILE_ENTRY_AGGREGATORS.lower():
                self.entry_files_to_download = [FILE_ENTRY_AGGREGATORS]
            if self.arguments['select'].lower() == FILE_ENTRY_DATASET_MAPPINGS.lower():
                self.entry_files_to_download = [FILE_ENTRY_DATASET_MAPPINGS]
            if self.arguments['select'].lower() == FILE_ENTRY_DATASET_RELATIONSHIPS.lower():
                self.entry_files_to_download = [FILE_ENTRY_DATASET_RELATIONSHIPS]
            if self.arguments['select'].lower() == FILE_ENTRY_ENTITY.lower():
                self.entry_files_to_download = [FILE_ENTRY_ENTITY]
            if self.arguments['select'].lower() == FILE_ENTRY_FILTERS.lower():
                self.entry_files_to_download = [FILE_ENTRY_FILTERS]
            if self.arguments['select'].lower() == FILE_ENTRY_ORDER.lower():
                self.entry_files_to_download = [FILE_ENTRY_ORDER]
            if self.arguments['select'].lower() == FILE_ENTRY_PATH.lower():
                self.entry_files_to_download = [FILE_ENTRY_PATH]
            if self.arguments['select'].lower() == FILE_ENTRY_HAVING.lower():
                self.entry_files_to_download = [FILE_ENTRY_HAVING]
            if self.arguments['select'].lower() == FILE_ENTRY_DV_ENTITY.lower():
                self.entry_files_to_download = [FILE_ENTRY_DV_ENTITY]
            if self.arguments['select'].lower() == FILE_ENTRY_DV_MAPPINGS.lower():
                self.entry_files_to_download = [FILE_ENTRY_DV_MAPPINGS]
            if self.arguments['select'].lower() == FILE_ENTRY_DV_PROPERTIES.lower():
                self.entry_files_to_download = [FILE_ENTRY_DV_PROPERTIES]
            if self.arguments['select'].lower() == FILE_ENTRY_FILES.lower():
                self.entry_files_to_download = [FILE_ENTRY_FILES]

        if 'owner' in self.arguments:
            self.owner_to_download = self.arguments['owner']

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()
        self._initialize_download_engine()

        self.log.log(self.engine_name, "Start downloading Metadata Entry", LOG_LEVEL_INFO)

        self.metadata_actual = self.load_metadata(load_om=False, load_entry=True, load_ref=False, load_im=False, owner=self.owner_to_download)

        # ENTRY_ENTITY
        content = []
        if FILE_ENTRY_ENTITY in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading ["+FILE_ENTRY_ENTITY+"]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_ENTITY[:-1])
            for registry in self.metadata_actual.entry_entity:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_ENTITY)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_ENTITY + "]", LOG_LEVEL_INFO)

        # ENTRY_DATASET_MAPPINGS
        content = []
        if FILE_ENTRY_DATASET_MAPPINGS in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_DATASET_MAPPINGS + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_DATASET_MAPPINGS[:-1])
            for registry in self.metadata_actual.entry_dataset_mappings:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_DATASET_MAPPINGS)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_DATASET_MAPPINGS + "]", LOG_LEVEL_INFO)

            file_controller_final.write_file(content)

        # ENTRY_DATASET_RELATIONSHIPS
        content = []
        if FILE_ENTRY_DATASET_RELATIONSHIPS in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_DATASET_RELATIONSHIPS + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_DATASET_RELATIONSHIPS[:-1])
            for registry in self.metadata_actual.entry_dataset_relationship:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_DATASET_RELATIONSHIPS)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_DATASET_RELATIONSHIPS + "]", LOG_LEVEL_INFO)

        # ENTRY_ORDER
        content = []
        if FILE_ENTRY_ORDER in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_ORDER + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_ORDER[:-1])
            for registry in self.metadata_actual.entry_order:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_ORDER)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_ORDER + "]", LOG_LEVEL_INFO)

        # ENTRY_AGGREGATOR
        content = []
        if FILE_ENTRY_AGGREGATORS in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_AGGREGATORS + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_AGGREGATORS[:-1])
            for registry in self.metadata_actual.entry_aggregators:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_AGGREGATORS)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_AGGREGATORS + "]", LOG_LEVEL_INFO)

        # ENTRY_PATH
        content = []
        if FILE_ENTRY_PATH in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_PATH + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_PATH[:-1])
            for registry in self.metadata_actual.entry_path:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_PATH)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_PATH + "]", LOG_LEVEL_INFO)

        # ENTRY_FILTERS
        content = []
        if FILE_ENTRY_FILTERS in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_FILTERS + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_PATH[:-1])
            for registry in self.metadata_actual.entry_filters:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_FILTERS)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_FILTERS + "]", LOG_LEVEL_INFO)

        # ENTRY_HAVING
        content = []
        if FILE_ENTRY_HAVING in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_HAVING + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_HAVING[:-1])
            for registry in self.metadata_actual.entry_having:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_HAVING)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_HAVING + "]", LOG_LEVEL_INFO)

        # ENTRY_DV_ENTITY
        content = []
        if FILE_ENTRY_DV_ENTITY in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_DV_ENTITY + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_DV_ENTITY[:-1])
            for registry in self.metadata_actual.entry_dv_entity:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_DV_ENTITY)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_DV_ENTITY + "]", LOG_LEVEL_INFO)

        # ENTRY_DV_MAPPINGS
        content = []
        if FILE_ENTRY_DV_MAPPINGS in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_DV_MAPPINGS + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_DV_MAPPINGS[:-1])
            for registry in self.metadata_actual.entry_dv_mappings:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_DV_MAPPINGS)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_DV_MAPPINGS + "]", LOG_LEVEL_INFO)

        # ENTRY_DV_PROPERTIES
        content = []
        if FILE_ENTRY_DV_PROPERTIES in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_DV_PROPERTIES + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_DV_PROPERTIES[:-1])
            for registry in self.metadata_actual.entry_dv_properties:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_DV_PROPERTIES)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_DV_PROPERTIES + "]", LOG_LEVEL_INFO)

        # ENTRY_FILES
        content = []
        if FILE_ENTRY_FILES in self.entry_files_to_download:
            self.log.log(self.engine_name, "Downloading [" + FILE_ENTRY_FILES + "]", LOG_LEVEL_INFO)
            content.append(COLUMNS_ENTRY_FILES[:-1])
            for registry in self.metadata_actual.entry_files:
                content.append(registry.get()[:-1])
            file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_CSV)
            file_controller_final.set_file_location(os.path.join(ACTUAL_PATH, ENTRY_FILES_PATH), FILE_ENTRY_FILES)
            file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)
            file_controller_final.write_file(content)
            self.log.log(self.engine_name, "Finish download for [" + FILE_ENTRY_FILES + "]", LOG_LEVEL_INFO)



        super().finish_execution()