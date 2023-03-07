from metamorf.engines.engine import Engine
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.metadata import Metadata
import re
from metamorf.tools.query import Query

class EngineProcess(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Process"
        self.engine_command = "process"
        self.module_elt_active = False
        self.module_elt_some_sources_to_one_target = "union"
        self.module_dv_active = False
        self.module_dv_some_sources_to_one_target = "split"
        self.module_dv_char_separator_naming = "_"

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()

        if len(self.modules_to_execute) == 0:
            self.log.log(self.engine_name, "No Modules are Active - No metadata will be processed", LOG_LEVEL_WARNING)
            super().finish_execution()
            return

        self.connection = ConnectionFactory().get_connection(self.configuration_file['data']['connection_type'])
        self.connection_metadata = ConnectionFactory().get_connection(self.configuration_file['metadata']['connection_type'])
        self.metadata_actual = self.load_metadata(load_om=True, load_entry=True, load_ref=True, load_im=False, owner=self.owner)
        self.metadata_to_load = Metadata(self.log)

        self.get_next_ids()

        #TODO: Validate Metadata

        # Process Metadata and get new Metadata to update database
        if MODULE_DV in self.modules_to_execute or MODULE_ELT in self.modules_to_execute: self.process_common()
        if MODULE_ELT in self.modules_to_execute: self.process_elt()
        if MODULE_DV in self.modules_to_execute: self.process_dv()

        self.log.log(self.engine_name, "Starting to process Historical Metadata from ELT Module", LOG_LEVEL_INFO)
        self.process_elt_historical()
        self.log.log(self.engine_name, "Finished to process Historical Metadata from ELT Module", LOG_LEVEL_INFO)

        self.connection.close()
        self.upload_metadata()

        super().finish_execution()

    def nvl(self, number, default):
        if number is None: return default
        return number

    def get_next_ids(self):
        self.log.log(self.engine_name, "Starting to get id's from database", LOG_LEVEL_INFO)
        connection = ConnectionFactory().get_connection(self.configuration_file['metadata']['connection_type'])
        connection.setup_connection(self.configuration_file['metadata'], self.log)

        # DATASET
        query = Query()
        query.set_type(QUERY_TYPE_SELECT)
        query.set_select_columns(['MAX('+COLUMNS_OM_DATASET[0]+')'])
        query.set_from_tables(TABLE_OM_DATASET)
        connection.execute(str(query))
        self.next_id_dataset = self.nvl(connection.get_query_result()[0][0], 0) + 1

        # DATASET_PATH
        query = Query()
        query.set_type(QUERY_TYPE_SELECT)
        query.set_select_columns(['MAX(' + COLUMNS_OM_DATASET_PATH[0] + ')'])
        query.set_from_tables(TABLE_OM_DATASET_PATH)
        connection.execute(str(query))
        self.next_id_path = self.nvl(connection.get_query_result()[0][0], 0) + 1

        # DATASET_SPECIFICATION
        query = Query()
        query.set_type(QUERY_TYPE_SELECT)
        query.set_select_columns(['MAX(' + COLUMNS_OM_DATASET_SPECIFICATION[0] + ')'])
        query.set_from_tables(TABLE_OM_DATASET_SPECIFICATION)
        connection.execute(str(query))
        self.next_id_dataset_spec = self.nvl(connection.get_query_result()[0][0], 0) + 1

        # DATASET_RELATIONSHIPS
        query = Query()
        query.set_type(QUERY_TYPE_SELECT)
        query.set_select_columns(['MAX(' + COLUMNS_OM_DATASET_RELATIONSHIPS[0] + ')'])
        query.set_from_tables(TABLE_OM_DATASET_RELATIONSHIPS)
        connection.execute(str(query))
        self.next_id_relationship = self.nvl(connection.get_query_result()[0][0], 0) + 1

        # DATASET_AGG
        query = Query()
        query.set_type(QUERY_TYPE_SELECT)
        query.set_select_columns(['MAX(' + COLUMNS_OM_DATASET_T_AGG[0] + ')'])
        query.set_from_tables(TABLE_OM_DATASET_T_AGG)
        connection.execute(str(query))
        self.next_id_agg = self.nvl(connection.get_query_result()[0][0], 0) + 1

        # DATASET_ORDER
        query = Query()
        query.set_type(QUERY_TYPE_SELECT)
        query.set_select_columns(['MAX(' + COLUMNS_OM_DATASET_T_ORDER[0] + ')'])
        query.set_from_tables(TABLE_OM_DATASET_T_ORDER)
        connection.execute(str(query))
        self.next_id_t_order = self.nvl(connection.get_query_result()[0][0], 0) + 1

        # DATASET_DISTINCT
        query = Query()
        query.set_type(QUERY_TYPE_SELECT)
        query.set_select_columns(['MAX(' + COLUMNS_OM_DATASET_T_DISTINCT[0] + ')'])
        query.set_from_tables(TABLE_OM_DATASET_T_DISTINCT)
        connection.execute(str(query))
        self.next_id_t_distinct = self.nvl(connection.get_query_result()[0][0], 0) + 1

        # DATASET_MAPPING
        query = Query()
        query.set_type(QUERY_TYPE_SELECT)
        query.set_select_columns(['MAX(' + COLUMNS_OM_DATASET_T_MAPPING[0] + ')'])
        query.set_from_tables(TABLE_OM_DATASET_T_MAPPING)
        connection.execute(str(query))
        self.next_id_t_mapping = self.nvl(connection.get_query_result()[0][0], 0) + 1

        # DATASET_FILTER
        query = Query()
        query.set_type(QUERY_TYPE_SELECT)
        query.set_select_columns(['MAX(' + COLUMNS_OM_DATASET_T_FILTER[0] + ')'])
        query.set_from_tables(TABLE_OM_DATASET_T_FILTER)
        connection.execute(str(query))
        self.next_id_t_filter = self.nvl(connection.get_query_result()[0][0], 0) + 1

        # DATASET_HAVING
        query = Query()
        query.set_type(QUERY_TYPE_SELECT)
        query.set_select_columns(['MAX(' + COLUMNS_OM_DATASET_T_HAVING[0] + ')'])
        query.set_from_tables(TABLE_OM_DATASET_T_HAVING)
        connection.execute(str(query))
        self.next_id_t_having = self.nvl(connection.get_query_result()[0][0], 0) + 1
        self.log.log(self.engine_name, "Finished to get id's from database", LOG_LEVEL_INFO)

    def process_common(self):
        self.log.log(self.engine_name, "Starting to process Metadata from all modules", LOG_LEVEL_INFO)
        self.process_elt_path()
        self.process_elt_sources()
        self.log.log(self.engine_name, "Finished to process Metadata from all modules", LOG_LEVEL_INFO)

    def process_elt(self):
        self.log.log(self.engine_name, "Starting to process Metadata from ELT Module", LOG_LEVEL_INFO)

        self.process_elt_execution()
        self.process_elt_order()
        self.process_elt_relationship()
        self.process_elt_aggregator()
        self.process_elt_distinct()
        self.process_elt_mapping()
        self.process_elt_filter()
        self.process_elt_having()

        self.log.log(self.engine_name, "Finished to process Metadata from ELT Module", LOG_LEVEL_INFO)

    def process_elt_path(self):
        # Input Paths
        next_id_path = self.next_id_path
        path_loaded = []
        for processing_path in self.metadata_actual.entry_path:
            path_already = self.metadata_actual.get_path_from_database_and_schema(processing_path.database_name,
                                                                                  processing_path.schema_name)
            if [processing_path.database_name, processing_path.schema_name] in path_loaded: continue
            if path_already is None:
                id_path = next_id_path
                next_id_path += 1
                new_path = [id_path, processing_path.database_name, processing_path.schema_name, self.owner,
                            self.connection_metadata.get_sysdate_value(), "NULL"]
                self.metadata_to_load.add_om_dataset_path([new_path])
                path_loaded.append([processing_path.database_name, processing_path.schema_name])
            else:
                if processing_path.database_name == path_already.database_name and str(
                        processing_path.schema_name) == str(path_already.schema_name):
                    same_path = [path_already.id_path, path_already.database_name, path_already.schema_name,
                                 path_already.meta_owner, "'" + str(path_already.start_date) + "'", "NULL"]
                    self.metadata_to_load.add_om_dataset_path([same_path])
                    path_loaded.append([path_already.database_name, path_already.schema_name])
                else:
                    close_path = [path_already.id_path, path_already.database_name, path_already.schema_name,
                                  path_already.meta_owner, "'" + str(path_already.start_date) + "'",
                                  self.connection_metadata.get_sysdate_value()]
                    self.metadata_to_load.add_om_dataset_path([close_path])
                    path_loaded.append([path_already.database_name, path_already.schema_name])

                    id_path = next_id_path
                    next_id_path += 1
                    new_path = [id_path, processing_path.database_name, processing_path.schema_name, self.owner,
                                self.connection_metadata.get_sysdate_value(), "NULL"]
                    self.metadata_to_load.add_om_dataset_path([new_path])
                    path_loaded.append([processing_path.database_name, processing_path.schema_name])

        for path in [x for x in self.metadata_actual.om_dataset_path if x.end_date is None]:
            if [path.database_name, path.schema_name] not in path_loaded:
                close_path = [path.id_path, path.database_name, path.schema_name, path.meta_owner,
                              "'" + str(path.start_date) + "'", self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_path([close_path])

    def process_elt_execution(self):
        execution_added = []
        for entry in [x for x in self.metadata_actual.entry_entity if x.entity_type in (ENTITY_TB, ENTITY_VIEW)]:
            new_dataset_id = self.metadata_to_load.get_dataset_from_dataset_name(entry.table_name).id_dataset
            id_query_type = self.metadata_actual.get_query_type_from_query_type_name(entry.strategy).id_query_type

            old_dataset_execution = self.metadata_actual.get_dataset_execution_from_id_dataset(new_dataset_id)

            if old_dataset_execution is None:
                new_dataset_execution = [new_dataset_id, id_query_type, self.owner, self.connection_metadata.get_sysdate_value(), "NULL"]
                self.metadata_to_load.add_om_dataset_execution([new_dataset_execution])
                execution_added.append(new_dataset_id)
            else:
                if old_dataset_execution.id_query_type == id_query_type:
                    existent_dataset_execution = [old_dataset_execution.id_dataset, old_dataset_execution.id_query_type, self.owner, "'"+str(old_dataset_execution.start_date)+"'", "NULL"]
                    self.metadata_to_load.add_om_dataset_execution([existent_dataset_execution])
                    execution_added.append(old_dataset_execution.id_dataset)
                else:
                    existent_dataset_execution = [old_dataset_execution.id_dataset, old_dataset_execution.id_query_type, self.owner, "'"+str(old_dataset_execution.start_date)+"'", self.connection_metadata.get_sysdate_value()]
                    self.metadata_to_load.add_om_dataset_execution([existent_dataset_execution])

                    new_dataset_execution = [new_dataset_id, id_query_type, self.owner, self.connection_metadata.get_sysdate_value(), "NULL"]
                    self.metadata_to_load.add_om_dataset_execution([new_dataset_execution])
                    execution_added.append(new_dataset_id)

        for execution in [x for x in self.metadata_actual.om_dataset_execution if x.end_date is None]:
            if execution.id_dataset not in execution_added:
                not_arriving_dataset_execution = [execution.id_dataset, execution.id_query_type,
                                              self.owner, "'" + str(execution.start_date) + "'",
                                              self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_execution([not_arriving_dataset_execution])

    def process_dv_entities(self):
        next_id_dataset = self.next_id_dataset
        next_id_dataset_spec = self.next_id_dataset_spec
        sources_loaded = []
        sources_specs_loaded = []

        # Generate HUBS
        for entity in self.metadata_actual.entry_entity:
            if entity.entity_type == ENTITY_HUB and entity.table_name not in sources_loaded:
                dataset = self.metadata_actual.get_dataset_from_dataset_name(entity.table_name)
                id_entity_type = (self.metadata_actual.get_entity_type_from_entity_type_name(ENTITY_HUB)).id_entity_type
                end_date = "NULL"

                if dataset is None:
                    # If the dataset doesn't exist it will be added
                    id_dataset = next_id_dataset
                    next_id_dataset += 1
                    entry_path = self.metadata_actual.get_entry_path_from_cod_path(entity.cod_path)
                    id_path = (self.metadata_to_load.get_path_from_database_and_schema(entry_path.database_name, entry_path.schema_name)).id_path
                    start_date = self.connection_metadata.get_sysdate_value()
                    new_source = [id_dataset, entity.table_name, id_entity_type, id_path, self.owner, start_date, end_date]
                    self.metadata_to_load.add_om_dataset([new_source])

                else:
                    # If the dataset exists, we need to verify if any of the attribute has changed
                    entry_path = self.metadata_actual.get_entry_path_from_cod_path(entity.cod_path)

                    # If the dataset has the same ENTITY TYPE and PATH => add the same dataset
                    if dataset.id_path == (self.metadata_to_load.get_path_from_database_and_schema(entry_path.database_name, entry_path.schema_name)).id_path \
                            and dataset.id_entity_type == self.metadata_actual.get_entity_type_from_entity_type_name(ENTITY_HUB).id_entity_type:
                        close_source = [dataset.id_dataset, dataset.dataset_name, dataset.id_entity_type,
                                        dataset.id_path, dataset.meta_owner, "'" + str(dataset.start_date) + "'",
                                        "NULL"]
                        self.metadata_to_load.add_om_dataset([close_source])


                    # If the path or de entity type has changed, the actual needs to be closed and add the actual
                    else:
                        # Close the actual one
                        close_source = [dataset.id_dataset, dataset.dataset_name, dataset.id_entity_type,
                                        dataset.id_path,
                                        dataset.meta_owner, "'" + str(dataset.start_date) + "'",
                                        self.connection_metadata.get_sysdate_value()]
                        self.metadata_to_load.add_om_dataset([close_source])

                        id_dataset = next_id_dataset
                        next_id_dataset += 1
                        id_path = (self.metadata_to_load.get_path_from_database_and_schema(entry_path.database_name,
                                                                                           entry_path.schema_name)).id_path
                        # Add the updated one
                        updated_source = [id_dataset, dataset.dataset_name,
                                          self.metadata_actual.get_entity_type_from_entity_type_name(
                                              ENTITY_HUB).id_entity_type,
                                          id_path, dataset.meta_owner, self.connection_metadata.get_sysdate_value(),
                                          "NULL"]
                        self.metadata_to_load.add_om_dataset([updated_source])
                        dataset = self.metadata_to_load.get_dataset_from_dataset_name(dataset.dataset_name)

                sources_loaded.append(entity.table_name)

                # Load Dataset Specs from DV Entity


        pass

    def process_elt_sources(self):
        ######################## LOAD SOURCES and SPECIFICATIONS ########################
        next_id_dataset = self.next_id_dataset
        next_id_dataset_spec = self.next_id_dataset_spec
        sources_loaded = []
        sources_specs_loaded = []

        # Input Sources
        for entity in self.metadata_actual.entry_entity:
            if entity.entity_type == ENTITY_SRC and entity.table_name not in sources_loaded:
                dataset = self.metadata_actual.get_dataset_from_dataset_name(entity.table_name)
                id_entity_type = (self.metadata_actual.get_entity_type_from_entity_type_name(ENTITY_SRC)).id_entity_type
                end_date = "NULL"

                if dataset is None:
                    # If the dataset doesn't exist it will be added
                    id_dataset = next_id_dataset
                    next_id_dataset += 1
                    entry_path = self.metadata_actual.get_entry_path_from_cod_path(entity.cod_path)
                    id_path = (self.metadata_to_load.get_path_from_database_and_schema(entry_path.database_name,
                                                                                       entry_path.schema_name)).id_path
                    start_date = self.connection_metadata.get_sysdate_value()
                    new_source = [id_dataset, entity.table_name, id_entity_type, id_path, self.owner, start_date,
                                  end_date]
                    self.metadata_to_load.add_om_dataset([new_source])

                else:
                    # If the dataset exists, we need to verify if any of the attribute has changed
                    entry_path = self.metadata_actual.get_entry_path_from_cod_path(entity.cod_path)

                    # If the dataset has the same ENTITY TYPE and PATH => add the same dataset
                    if dataset.id_path == (self.metadata_to_load.get_path_from_database_and_schema(entry_path.database_name,entry_path.schema_name)).id_path \
                            and dataset.id_entity_type == self.metadata_actual.get_entity_type_from_entity_type_name(ENTITY_SRC).id_entity_type:
                        id_dataset = dataset.id_dataset
                        id_path = dataset.id_path
                        close_source = [dataset.id_dataset, dataset.dataset_name, dataset.id_entity_type,
                                        dataset.id_path, dataset.meta_owner, "'" + str(dataset.start_date) + "'",
                                        "NULL"]
                        self.metadata_to_load.add_om_dataset([close_source])


                    # If the path or de entity type has changed, the actual needs to be closed and add the actual
                    else:
                        # Close the actual one
                        close_source = [dataset.id_dataset, dataset.dataset_name, dataset.id_entity_type,
                                        dataset.id_path,
                                        dataset.meta_owner, "'" + str(dataset.start_date) + "'",
                                        self.connection_metadata.get_sysdate_value()]
                        self.metadata_to_load.add_om_dataset([close_source])

                        id_dataset = next_id_dataset
                        next_id_dataset += 1
                        id_path = (self.metadata_to_load.get_path_from_database_and_schema(entry_path.database_name,
                                                                                           entry_path.schema_name)).id_path
                        # Add the updated one
                        updated_source = [id_dataset, dataset.dataset_name,
                                        self.metadata_actual.get_entity_type_from_entity_type_name(
                                            ENTITY_SRC).id_entity_type,
                                        id_path, dataset.meta_owner, self.connection_metadata.get_sysdate_value(),
                                        "NULL"]
                        self.metadata_to_load.add_om_dataset([updated_source])
                        dataset = self.metadata_to_load.get_dataset_from_dataset_name(dataset.dataset_name)

                sources_loaded.append(entity.table_name)

                # Get Dataset Specifications from Data Database
                variable_connection = self.configuration_file['data']['connection_type'].lower() + "_database"
                configuration_connection_data = self.configuration_file['data']
                configuration_connection_data[variable_connection] = (self.metadata_to_load.get_path_from_id_path(id_path)).database_name
                self.connection.setup_connection(configuration_connection_data, self.log)
                table_definition = self.connection.get_table_columns_definition(entity.table_name)

                # Source Specification
                if dataset is None:
                    # If the dataset is new, all the dataset specification will be added
                    for table_definition_spec in table_definition:
                        id_dataset_spec = next_id_dataset_spec
                        next_id_dataset_spec += 1
                        key_type_name = KEY_TYPE_NULL
                        if table_definition_spec.is_pk == 1: key_type_name = KEY_TYPE_PRIMARY_KEY
                        id_key_type = (self.metadata_actual.get_key_type_from_key_type_name(key_type_name)).id_key_type
                        start_date = self.connection_metadata.get_sysdate_value()
                        end_date = "NULL"

                        new_dataset_specification = [id_dataset_spec, id_dataset, id_key_type,
                                                     table_definition_spec.column_name,
                                                     table_definition_spec.column_type, table_definition_spec.id,
                                                     table_definition_spec.is_nullable, table_definition_spec.length,
                                                     table_definition_spec.precision, table_definition_spec.scale,
                                                     self.owner, start_date, end_date]
                        self.metadata_to_load.add_om_dataset_specification([new_dataset_specification])
                        sources_specs_loaded.append([id_dataset, table_definition_spec.column_name])

                else:
                    # Source specification existent
                    # Update any column
                    for existent_col in [x for x in self.metadata_actual.om_dataset_specification if x.id_dataset == dataset.id_dataset and x.end_date is None]:
                        finded = False
                        for table_definition_spec in table_definition:
                            key_type_name = KEY_TYPE_NULL
                            if table_definition_spec.is_pk == 1: key_type_name = KEY_TYPE_PRIMARY_KEY
                            id_key_type = (self.metadata_actual.get_key_type_from_key_type_name(key_type_name)).id_key_type

                            checksum_existent = str(
                                existent_col.id_key_type) + existent_col.column_name + existent_col.column_type + \
                                                str(existent_col.ordinal_position) + str(
                                existent_col.is_nullable) + str(existent_col.length) + \
                                                str(existent_col.precision) + str(existent_col.scale)
                            checksum_new = str(
                                id_key_type) + table_definition_spec.column_name + table_definition_spec.column_type + \
                                           str(table_definition_spec.id) + str(table_definition_spec.is_nullable) + str(
                                table_definition_spec.length) + \
                                           str(table_definition_spec.precision) + str(table_definition_spec.scale)
                            if checksum_new == checksum_existent:
                                finded = True
                                # Column that exists already, if on origin is the same, we maintain all the info
                                close_dataset_specification = [existent_col.id_dataset_spec, dataset.id_dataset,
                                                               existent_col.id_key_type,
                                                               existent_col.column_name,
                                                               existent_col.column_type,
                                                               existent_col.ordinal_position, existent_col.is_nullable,
                                                               existent_col.length,
                                                               existent_col.precision, existent_col.scale,
                                                               existent_col.meta_owner,
                                                               "'" + str(existent_col.start_date) + "'",
                                                               "NULL"]
                                self.metadata_to_load.add_om_dataset_specification([close_dataset_specification])
                                sources_specs_loaded.append([existent_col.id_dataset, existent_col.column_name])

                        # Column that is no more on source
                        if not finded:
                            close_dataset_specification = [existent_col.id_dataset_spec, existent_col.id_dataset,
                                                           existent_col.id_key_type,
                                                           existent_col.column_name,
                                                           existent_col.column_type,
                                                           existent_col.ordinal_position, existent_col.is_nullable,
                                                           existent_col.length,
                                                           existent_col.precision, existent_col.scale,
                                                           existent_col.meta_owner,
                                                           "'" + str(existent_col.start_date) + "'",
                                                           self.connection_metadata.get_sysdate_value()]
                            self.metadata_to_load.add_om_dataset_specification([close_dataset_specification])
                            sources_specs_loaded.append([existent_col.id_dataset, existent_col.column_name])

                    # Add new columns
                    for table_definition_spec in table_definition:
                        finded = False
                        for existent_col in [x for x in self.metadata_actual.om_dataset_specification if x.id_dataset == dataset.id_dataset and x.end_date is None]:
                            key_type_name = KEY_TYPE_NULL
                            if table_definition_spec.is_pk == 1: key_type_name = KEY_TYPE_PRIMARY_KEY
                            id_key_type = (
                                self.metadata_actual.get_key_type_from_key_type_name(key_type_name)).id_key_type

                            checksum_existent = str(
                                existent_col.id_key_type) + existent_col.column_name + existent_col.column_type + \
                                                str(existent_col.ordinal_position) + str(
                                existent_col.is_nullable) + str(existent_col.length) + \
                                                str(existent_col.precision) + str(existent_col.scale)
                            checksum_new = str(
                                id_key_type) + table_definition_spec.column_name + table_definition_spec.column_type + \
                                           str(table_definition_spec.id) + str(table_definition_spec.is_nullable) + str(
                                table_definition_spec.length) + \
                                           str(table_definition_spec.precision) + str(table_definition_spec.scale)
                            if checksum_new == checksum_existent:
                                finded = True
                                break
                        # New column is added on source
                        if not finded:
                            id_dataset_spec = next_id_dataset_spec
                            next_id_dataset_spec += 1
                            key_type_name = KEY_TYPE_NULL
                            if table_definition_spec.is_pk == 1: key_type_name = KEY_TYPE_PRIMARY_KEY
                            id_key_type = (
                                self.metadata_actual.get_key_type_from_key_type_name(key_type_name)).id_key_type
                            start_date = self.connection_metadata.get_sysdate_value()
                            end_date = "NULL"

                            new_dataset_specification = [id_dataset_spec, dataset.id_dataset, id_key_type,
                                                         table_definition_spec.column_name,
                                                         table_definition_spec.column_type, table_definition_spec.id,
                                                         table_definition_spec.is_nullable,
                                                         table_definition_spec.length,
                                                         table_definition_spec.precision, table_definition_spec.scale,
                                                         self.owner, start_date, end_date]
                            self.metadata_to_load.add_om_dataset_specification([new_dataset_specification])
                            sources_specs_loaded.append([dataset.id_dataset, table_definition_spec.column_name])

        # Close sources that not arrive anymore
        for dataset in [x for x in self.metadata_actual.om_dataset if x.id_entity_type == self.metadata_actual.get_entity_type_from_entity_type_name(ENTITY_SRC).id_entity_type]:
            if dataset.dataset_name not in sources_loaded and dataset.end_date is None:
                close_source = [dataset.id_dataset, dataset.dataset_name, dataset.id_entity_type,
                                dataset.id_path, "'" + dataset.meta_owner + "'", "'" + str(dataset.start_date) + "'",
                                self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset([close_source])

        ######################## LOAD ALL OTHER TABLES and SPECIFICATIONS ########################
        # Input Sources
        tmp_loaded = []
        tmp_specs_loaded = []

        for entity in self.metadata_actual.entry_entity:

            if (entity.entity_type == ENTITY_TB or entity.entity_type == ENTITY_WITH or entity.entity_type == ENTITY_VIEW) and entity.table_name not in tmp_loaded:
                dataset = self.metadata_actual.get_dataset_from_dataset_name(entity.table_name)
                id_entity_type = (self.metadata_actual.get_entity_type_from_entity_type_name(
                    entity.entity_type.upper())).id_entity_type
                end_date = "NULL"
                # New Temporal
                if dataset is None:
                    # New Source
                    id_dataset = next_id_dataset
                    next_id_dataset += 1
                    entry_path = self.metadata_actual.get_entry_path_from_cod_path(entity.cod_path)
                    id_path = (self.metadata_to_load.get_path_from_database_and_schema(entry_path.database_name,
                                                                                       entry_path.schema_name)).id_path
                    start_date = self.connection_metadata.get_sysdate_value()
                    new_source = [id_dataset, entity.table_name, id_entity_type, id_path, self.owner, start_date,
                                  end_date]
                    self.metadata_to_load.add_om_dataset([new_source])
                    tmp_loaded.append([entity.table_name, id_entity_type, id_path])
                # Update TMP
                else:
                    entry_path = self.metadata_actual.get_entry_path_from_cod_path(entity.cod_path)
                    # If it's the same
                    if dataset.id_path == (self.metadata_to_load.get_path_from_database_and_schema(entry_path.database_name,
                                                                            entry_path.schema_name)).id_path \
                            and self.metadata_actual.get_entity_type_from_entity_type_name(
                        entity.entity_type).id_entity_type == dataset.id_entity_type:
                        id_path = dataset.id_path
                        close_source = [dataset.id_dataset, dataset.dataset_name, dataset.id_entity_type,
                                        dataset.id_path, dataset.meta_owner, "'" + str(dataset.start_date) + "'",
                                        "NULL"]
                        self.metadata_to_load.add_om_dataset([close_source])
                        tmp_loaded.append([dataset.dataset_name, dataset.id_entity_type, dataset.id_path])
                        id_dataset = dataset.id_dataset

                    # If the path or the entity has changed, the actual needs to be closed and add the actual
                    else:
                        if (dataset.id_entity_type != self.metadata_actual.get_entity_type_from_entity_type_name(ENTITY_SRC).id_entity_type):
                            close_source = [dataset.id_dataset, dataset.dataset_name, dataset.id_entity_type,
                                            dataset.id_path, dataset.meta_owner, "'" + str(dataset.start_date) + "'",
                                            self.connection_metadata.get_sysdate_value()]
                            print(close_source)
                            self.metadata_to_load.add_om_dataset([close_source])
                            tmp_loaded.append([dataset.dataset_name, dataset.id_entity_type, dataset.id_path])

                        id_dataset = next_id_dataset
                        next_id_dataset += 1
                        id_path = (self.metadata_to_load.get_path_from_database_and_schema(entry_path.database_name,
                                                                                           entry_path.schema_name)).id_path
                        updated_source = [id_dataset, dataset.dataset_name,
                                        self.metadata_actual.get_entity_type_from_entity_type_name(
                                            entity.entity_type).id_entity_type,
                                        id_path, dataset.meta_owner, self.connection_metadata.get_sysdate_value(),
                                        "NULL"]
                        self.metadata_to_load.add_om_dataset([updated_source])
                        dataset = self.metadata_to_load.get_dataset_from_dataset_name(dataset.dataset_name)
                        tmp_loaded.append([dataset.dataset_name, dataset.id_entity_type, id_path])

                # Get Dataset Specifications from Data Database
                variable_connection = self.configuration_file['data']['connection_type'].lower() + "_database"
                configuration_connection_data = self.configuration_file['data']
                configuration_connection_data[variable_connection] = (
                    self.metadata_to_load.get_path_from_id_path(id_path)).database_name
                # self.connection.setup_connection(configuration_connection_data, self.log)
                table_definition = self.metadata_actual.get_cols_from_cod_entity_on_entry(entity.cod_entity)
                # Source Specification
                if dataset is None:
                    # New Sources Specification
                    for table_definition_spec in table_definition:
                        id_dataset_spec = next_id_dataset_spec
                        next_id_dataset_spec += 1
                        key_type_name = KEY_TYPE_NULL
                        if table_definition_spec.is_pk == 1: key_type_name = KEY_TYPE_PRIMARY_KEY
                        id_key_type = (
                            self.metadata_actual.get_key_type_from_key_type_name(key_type_name)).id_key_type
                        start_date = self.connection_metadata.get_sysdate_value()
                        end_date = "NULL"

                        new_dataset_specification = [id_dataset_spec, id_dataset, id_key_type,
                                                     table_definition_spec.column_name,
                                                     table_definition_spec.column_type, table_definition_spec.id,
                                                     table_definition_spec.is_nullable, table_definition_spec.length,
                                                     table_definition_spec.precision, table_definition_spec.scale,
                                                     self.owner, start_date, end_date]
                        self.metadata_to_load.add_om_dataset_specification([new_dataset_specification])
                        tmp_specs_loaded.append([id_dataset, table_definition_spec.column_name])

                else:
                    # Source specification existent
                    # Update any column
                    for existent_col in [x for x in self.metadata_actual.om_dataset_specification if x.id_dataset == dataset.id_dataset and x.end_date is None]:
                        finded = False
                        for table_definition_spec in table_definition:
                            key_type_name = KEY_TYPE_NULL
                            if table_definition_spec.is_pk == 1: key_type_name = KEY_TYPE_PRIMARY_KEY
                            id_key_type = (self.metadata_actual.get_key_type_from_key_type_name(key_type_name)).id_key_type

                            checksum_existent = str(
                                existent_col.id_key_type) + existent_col.column_name + existent_col.column_type + \
                                                str(existent_col.ordinal_position) + str(
                                existent_col.is_nullable) + str(existent_col.length) + \
                                                str(existent_col.precision) + str(existent_col.scale)
                            checksum_new = str(
                                id_key_type) + table_definition_spec.column_name + table_definition_spec.column_type + \
                                           str(table_definition_spec.id) + str(table_definition_spec.is_nullable) + str(
                                table_definition_spec.length) + str(table_definition_spec.precision) + str(
                                table_definition_spec.scale)
                            if checksum_new == checksum_existent:
                                finded = True
                                # Column that exists already, if on origin is the same, we maintain all the info
                                close_dataset_specification = [existent_col.id_dataset_spec,
                                                               dataset.id_dataset,
                                                               existent_col.id_key_type,
                                                               existent_col.column_name,
                                                               existent_col.column_type,
                                                               existent_col.ordinal_position,
                                                               existent_col.is_nullable,
                                                               existent_col.length,
                                                               existent_col.precision, existent_col.scale,
                                                               existent_col.meta_owner,
                                                               "'" + str(existent_col.start_date) + "'",
                                                               "NULL"]
                                self.metadata_to_load.add_om_dataset_specification([close_dataset_specification])
                                tmp_specs_loaded.append([dataset.id_dataset, existent_col.column_name])

                        # Column that is no more on source
                        if not finded:
                            close_dataset_specification = [existent_col.id_dataset_spec, existent_col.id_dataset,
                                                           existent_col.id_key_type,
                                                           existent_col.column_name,
                                                           existent_col.column_type,
                                                           existent_col.ordinal_position, existent_col.is_nullable,
                                                           existent_col.length,
                                                           existent_col.precision, existent_col.scale,
                                                           existent_col.meta_owner,
                                                           "'" + str(existent_col.start_date) + "'",
                                                           self.connection_metadata.get_sysdate_value()]
                            self.metadata_to_load.add_om_dataset_specification([close_dataset_specification])
                            tmp_specs_loaded.append([existent_col.id_dataset, existent_col.column_name])

                    # Add new columns
                    for table_definition_spec in table_definition:
                        finded = False
                        for existent_col in [x for x in self.metadata_actual.om_dataset_specification if x.id_dataset == dataset.id_dataset and x.end_date is None]:
                            key_type_name = KEY_TYPE_NULL
                            if table_definition_spec.is_pk == 1: key_type_name = KEY_TYPE_PRIMARY_KEY
                            id_key_type = (
                                self.metadata_actual.get_key_type_from_key_type_name(key_type_name)).id_key_type

                            checksum_existent = str(
                                existent_col.id_key_type) + existent_col.column_name + existent_col.column_type + \
                                                str(existent_col.ordinal_position) + str(
                                existent_col.is_nullable) + str(existent_col.length) + \
                                                str(existent_col.precision) + str(existent_col.scale)
                            checksum_new = str(
                                id_key_type) + table_definition_spec.column_name + table_definition_spec.column_type + \
                                           str(table_definition_spec.id) + str(table_definition_spec.is_nullable) + str(
                                table_definition_spec.length) + \
                                           str(table_definition_spec.precision) + str(table_definition_spec.scale)
                            if checksum_new == checksum_existent:
                                finded = True
                                break
                        # New column is added on source
                        if not finded:
                            id_dataset_spec = next_id_dataset_spec
                            next_id_dataset_spec += 1
                            key_type_name = KEY_TYPE_NULL
                            if table_definition_spec.is_pk == 1: key_type_name = KEY_TYPE_PRIMARY_KEY
                            id_key_type = (
                                self.metadata_actual.get_key_type_from_key_type_name(key_type_name)).id_key_type
                            start_date = self.connection_metadata.get_sysdate_value()
                            end_date = "NULL"

                            new_dataset_specification = [id_dataset_spec, dataset.id_dataset, id_key_type,
                                                         table_definition_spec.column_name,
                                                         table_definition_spec.column_type,
                                                         table_definition_spec.id,
                                                         table_definition_spec.is_nullable,
                                                         table_definition_spec.length,
                                                         table_definition_spec.precision, table_definition_spec.scale,
                                                         self.owner, start_date, end_date]
                            self.metadata_to_load.add_om_dataset_specification([new_dataset_specification])
                            tmp_specs_loaded.append([dataset.id_dataset, table_definition_spec.column_name])

        # Close tables that not arrive anymore
        for dataset in [x for x in self.metadata_actual.om_dataset if x.id_entity_type == self.metadata_actual.get_entity_type_from_entity_type_name(ENTITY_TB).id_entity_type
                        or x.id_entity_type== self.metadata_actual.get_entity_type_from_entity_type_name(ENTITY_WITH).id_entity_type]:
            if [dataset.dataset_name, dataset.id_entity_type, dataset.id_path] not in tmp_loaded and dataset.end_date is None:
                close_source = [dataset.id_dataset, dataset.dataset_name, dataset.id_entity_type,
                                dataset.id_path, dataset.meta_owner, "'" + str(dataset.start_date) + "'",
                                self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset([close_source])
        # Close Specifications that not arrive anymore
        for dataset_spec in self.metadata_actual.om_dataset_specification:
            if [dataset_spec.id_dataset, dataset_spec.column_name] not in tmp_specs_loaded and [dataset_spec.id_dataset, dataset_spec.column_name] not in sources_specs_loaded and dataset_spec.end_date is None:
                close_dataset_spec = [dataset_spec.id_dataset_spec, dataset_spec.id_dataset, dataset_spec.id_key_type,
                                      dataset_spec.column_name, dataset_spec.column_type, dataset_spec.ordinal_position,
                                      dataset_spec.is_nullable, dataset_spec.length,
                                      dataset_spec.precision,
                                      dataset_spec.scale, dataset_spec.meta_owner,
                                      "'" + str(dataset_spec.start_date) + "'", self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_specification([close_dataset_spec])

        self.next_id_dataset = next_id_dataset
        self.next_id_dataset_spec = next_id_dataset_spec

    def process_elt_order(self):
        next_id_t_order = self.next_id_t_order
        ######################## LOAD ORDER ########################
        # Input Orders
        order_loaded = []
        for order in self.metadata_actual.entry_order:
            dataset = self.metadata_to_load.get_dataset_from_dataset_name(self.metadata_actual.get_table_name_from_cod_entity_on_entry(order.cod_entity_target))
            dataset_src = self.metadata_to_load.get_dataset_from_dataset_name(self.metadata_actual.get_table_name_from_cod_entity_on_entry(order.cod_entity_src))
            dataset_spec = self.metadata_to_load.get_dataset_spec_from_id_dataset_and_column_name(dataset_src.id_dataset, order.column_name)

            # TODO: Incluir esta validación en todos los procesos -> Si no existe el campo -> sacar alerta
            # if dataset_spec is None: -> lanzar error
            order_existent = self.metadata_actual.get_order_from_id_dataset_and_id_dataset_spec_and_id_branch(dataset.id_dataset, dataset_spec.id_dataset_spec, order.num_branch)

            if order_existent is None:
                # New order
                id_t_order = next_id_t_order
                next_id_t_order += 1
                order_type = self.metadata_actual.get_order_type_from_order_type_value(order.order_type)
                start_date = self.connection_metadata.get_sysdate_value()
                new_order = [id_t_order, dataset.id_dataset, order.num_branch, dataset_spec.id_dataset_spec,
                             order_type.id_order_type, self.owner, start_date, 'NULL']
                self.metadata_to_load.add_om_dataset_t_order([new_order])
                order_loaded.append([dataset.id_dataset, order.num_branch, dataset_spec.id_dataset_spec])

            else:
                # Update order only
                # if the attributes are the diferent, the register will be closed
                if order_existent.id_order_type == self.metadata_actual.get_order_type_from_order_type_value(
                        order.order_type).id_order_type:
                    same_order = [order_existent.id_t_order, order_existent.id_dataset, order_existent.id_branch,
                                  order_existent.id_dataset_spec,
                                  order_existent.id_order_type, order_existent.meta_owner,
                                  "'" + str(order_existent.start_date) + "'", "NULL"]
                    self.metadata_to_load.add_om_dataset_t_order([same_order])
                    order_loaded.append(
                        [order_existent.id_dataset, order_existent.id_branch, order_existent.id_dataset_spec])
                else:
                    close_order = [order_existent.id_t_order, order_existent.id_dataset, order_existent.id_branch,
                                   order_existent.id_dataset_spec,
                                   order_existent.id_order_type, order_existent.meta_owner,
                                   "'" + str(order_existent.start_date) + "'", self.connection_metadata.get_sysdate_value()]
                    self.metadata_to_load.add_om_dataset_t_order([close_order])
                    order_loaded.append(
                        [order_existent.id_dataset, order_existent.id_branch, order_existent.id_dataset_spec])
                    id_t_order = next_id_t_order
                    next_id_t_order += 1
                    new_order = [id_t_order, dataset.id_dataset, order.num_branch, dataset_spec.id_dataset_spec,
                                 self.metadata_actual.get_order_type_from_order_type_value(
                                     order.order_type).id_order_type,
                                 self.owner, self.connection_metadata.get_sysdate_value(), "NULL"]
                    self.metadata_to_load.add_om_dataset_t_order([new_order])
                    order_loaded.append([dataset.id_dataset, order.num_branch, dataset_spec.id_dataset_spec])

        # Close order that not arrive anymore
        for order_type in [x for x in self.metadata_actual.om_dataset_t_order if x.end_date is None]:
            if [order_type.id_dataset, order_type.id_branch, order_type.id_dataset_spec] not in order_loaded:
                close_order = [order_type.id_t_order, order_type.id_dataset, order_type.id_branch,
                               order_type.id_dataset_spec,
                               order_type.id_order_type, order_type.meta_owner, "'" + str(order_type.start_date) + "'",
                               self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_t_order([close_order])

    def process_elt_relationship(self):
        next_id_relationship = self.next_id_relationship
        ######################## LOAD RELATIONSHIPS ########################
        # Input relationships
        relationships_loaded = []
        for relationship in self.metadata_actual.entry_dataset_relationship:
            dataset_master = self.metadata_to_load.get_dataset_from_dataset_name(
                self.metadata_actual.get_table_name_from_cod_entity_on_entry(relationship.cod_entity_master))
            dataset_spec_master = self.metadata_to_load.get_dataset_spec_from_id_dataset_and_column_name(
                dataset_master.id_dataset, relationship.column_name_master)

            dataset_detail = self.metadata_to_load.get_dataset_from_dataset_name(
                self.metadata_actual.get_table_name_from_cod_entity_on_entry(relationship.cod_entity_detail))
            dataset_spec_detail = self.metadata_to_load.get_dataset_spec_from_id_dataset_and_column_name(
                dataset_detail.id_dataset, relationship.column_name_detail)
            join_type = self.metadata_actual.get_join_type_from_join_name(relationship.relationship_type)

            relationship_existent = self.metadata_actual.get_relationship_from_id_dataset_spec_master_and_detail(
                dataset_spec_master.id_dataset_spec,
                dataset_spec_detail.id_dataset_spec)

            if relationship_existent is None:
                # New relationship
                id_relationship = next_id_relationship
                next_id_relationship += 1

                new_relationship = [id_relationship, dataset_spec_master.id_dataset_spec,
                                    dataset_spec_detail.id_dataset_spec,
                                    join_type.id_join_type, self.owner, self.connection_metadata.get_sysdate_value(), "NULL"]
                self.metadata_to_load.add_om_dataset_relationships([new_relationship])
                relationships_loaded.append([dataset_spec_master.id_dataset_spec, dataset_spec_detail.id_dataset_spec])

            else:
                # Update relationship
                if relationship_existent.id_join_type == join_type.id_join_type:
                    old_relationship = [relationship_existent.id_relationship,
                                        relationship_existent.id_dataset_spec_master,
                                        relationship_existent.id_dataset_spec_detail,
                                        relationship_existent.id_join_type, relationship_existent.meta_owner,
                                        "'" + str(relationship_existent.start_date) + "'", "NULL"]
                    self.metadata_to_load.add_om_dataset_relationships([old_relationship])
                    relationships_loaded.append(
                        [relationship_existent.id_dataset_spec_master, relationship_existent.id_dataset_spec_detail])
                else:
                    old_relationship = [relationship_existent.id_relationship,
                                        relationship_existent.id_dataset_spec_master,
                                        relationship_existent.id_dataset_spec_detail,
                                        relationship_existent.id_join_type, relationship_existent.meta_owner,
                                        "'" + str(relationship_existent.start_date) + "'",
                                        self.connection_metadata.get_sysdate_value()]
                    self.metadata_to_load.add_om_dataset_relationships([old_relationship])
                    relationships_loaded.append(
                        [relationship_existent.id_dataset_spec_master, relationship_existent.id_dataset_spec_detail])
                    id_relationship = next_id_relationship
                    next_id_relationship += 1
                    new_relationship = [id_relationship, dataset_spec_master.id_dataset_spec,
                                        dataset_spec_detail.id_dataset_spec,
                                        join_type.id_join_type, self.owner, self.connection_metadata.get_sysdate_value(), "NULL"]
                    self.metadata_to_load.add_om_dataset_relationships([new_relationship])
                    relationships_loaded.append(
                        [dataset_spec_master.id_dataset_spec, dataset_spec_detail.id_dataset_spec])

        # Close relationships that not arrive anymore
        for relationship in [x for x in self.metadata_actual.om_dataset_relationships if x.end_date is None]:
            if [relationship.id_dataset_spec_master, relationship.id_dataset_spec_detail] not in relationships_loaded:
                old_relationship = [relationship.id_relationship,
                                    relationship.id_dataset_spec_master,
                                    relationship.id_dataset_spec_detail,
                                    relationship.id_join_type, relationship.meta_owner,
                                    "'" + str(relationship.start_date) + "'", self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_relationships([old_relationship])

    def process_elt_aggregator(self):
        next_id_agg = self.next_id_agg
        ######################## LOAD AGGREGATOR ########################
        # Input Orders
        agg_loaded = []
        for agg in self.metadata_actual.entry_aggregators:
            dataset = self.metadata_to_load.get_dataset_from_dataset_name(self.metadata_actual.get_table_name_from_cod_entity_on_entry(agg.cod_entity_target))
            dataset_src = self.metadata_to_load.get_dataset_from_dataset_name(self.metadata_actual.get_table_name_from_cod_entity_on_entry(agg.cod_entity_src))
            dataset_spec = self.metadata_to_load.get_dataset_spec_from_id_dataset_and_column_name(dataset_src.id_dataset, agg.column_name)
            agg_existent = self.metadata_actual.get_aggregator_from_id_dataset_and_id_dataset_spec_and_id_branch(
                dataset.id_dataset, dataset_spec.id_dataset_spec, agg.num_branch)

            if agg_existent is None:
                id_t_agg = next_id_agg
                next_id_agg += 1
                new_agg = [id_t_agg, dataset.id_dataset, agg.num_branch, dataset_spec.id_dataset_spec, self.owner,
                           self.connection_metadata.get_sysdate_value(), "NULL"]
                self.metadata_to_load.add_om_dataset_t_agg([new_agg])
                agg_loaded.append([dataset.id_dataset, agg.num_branch, dataset_spec.id_dataset_spec])
            else:
                new_agg = [agg_existent.id_t_agg, agg_existent.id_dataset, agg_existent.id_branch,
                           agg_existent.id_dataset_spec,
                           agg_existent.meta_owner, "'" + str(agg_existent.start_date) + "'", "NULL"]
                self.metadata_to_load.add_om_dataset_t_agg([new_agg])
                agg_loaded.append([agg_existent.id_dataset, agg_existent.id_branch, agg_existent.id_dataset_spec])

        for agg in [x for x in self.metadata_actual.om_dataset_t_agg if x.end_date is None]:
            if [agg.id_dataset, agg.id_branch, agg.id_dataset_spec] not in agg_loaded:
                new_agg = [agg.id_t_agg, agg.id_dataset, agg.id_branch,
                           agg.id_dataset_spec,
                           agg.meta_owner, "'" + str(agg.start_date) + "'", self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_t_agg([new_agg])

    def process_elt_distinct(self):
        ######################## LOAD DISTINCT ########################
        # Input distinct
        next_id_t_distinct = self.next_id_t_distinct
        distinct_loaded = []
        for mapping in self.metadata_actual.entry_dataset_mappings:
            dataset = self.metadata_to_load.get_dataset_from_dataset_name(self.metadata_actual.get_table_name_from_cod_entity_on_entry(mapping.cod_entity_target))
            id_branch = mapping.num_branch
            distinct_existent = self.metadata_actual.get_distinct_from_id_dataset_and_branch(dataset.id_dataset, id_branch)
            sw_distinct = mapping.sw_distinct
            if [dataset.id_dataset, id_branch] in distinct_loaded: continue

            if distinct_existent is None:
                id_t_distinct = next_id_t_distinct
                next_id_t_distinct += 1
                new_distinct = [id_t_distinct, dataset.id_dataset, id_branch, sw_distinct, self.owner,
                                self.connection_metadata.get_sysdate_value(), "NULL"]
                self.metadata_to_load.add_om_dataset_t_distinct([new_distinct])
                distinct_loaded.append([dataset.id_dataset, id_branch])

            else:
                if sw_distinct == distinct_existent.sw_distinct:
                    existent_distinct = [distinct_existent.id_t_distinct, distinct_existent.id_dataset,
                                         distinct_existent.id_branch, distinct_existent.sw_distinct
                        , distinct_existent.meta_owner, "'" + str(distinct_existent.start_date) + "'", "NULL"]
                    self.metadata_to_load.add_om_dataset_t_distinct([existent_distinct])
                    distinct_loaded.append([distinct_existent.id_dataset, distinct_existent.id_branch])
                else:
                    existent_distinct = [distinct_existent.id_t_distinct, distinct_existent.id_dataset,
                                         distinct_existent.id_branch, distinct_existent.sw_distinct,
                                         distinct_existent.meta_owner,
                                         "'" + str(distinct_existent.start_date) + "'",
                                         self.connection_metadata.get_sysdate_value()]
                    self.metadata_to_load.add_om_dataset_t_distinct([existent_distinct])
                    distinct_loaded.append([distinct_existent.id_dataset, distinct_existent.id_branch])

                    id_t_distinct = next_id_t_distinct
                    next_id_t_distinct += 1
                    new_distinct = [id_t_distinct, dataset.id_dataset, id_branch, sw_distinct, self.owner,
                                    self.connection_metadata.get_sysdate_value(), "NULL"]
                    self.metadata_to_load.add_om_dataset_t_distinct([new_distinct])
                    distinct_loaded.append([dataset.id_dataset, id_branch])

        for distinct in [x for x in self.metadata_actual.om_dataset_t_distinct if x.end_date is None]:
            if [distinct.id_dataset, distinct.id_branch] not in distinct_loaded:
                close_distinct = [distinct.id_t_distinct, distinct.id_dataset, distinct.id_branch, distinct.sw_distinct
                    , distinct.meta_owner, "'" + str(distinct.start_date) + "'", self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_t_distinct([close_distinct])

    def process_elt_mapping(self):
        ######################## LOAD MAPPING ########################
        next_id_t_mapping = self.next_id_t_mapping

        mapping_loaded = []
        for mapping in self.metadata_actual.entry_dataset_mappings:
            dataset = self.metadata_to_load.get_dataset_from_dataset_name(self.metadata_actual.get_table_name_from_cod_entity_on_entry(mapping.cod_entity_target))
            dataset_spec = self.metadata_to_load.get_dataset_spec_from_id_dataset_and_column_name(dataset.id_dataset,
                                                                                                  mapping.column_name_target)
            id_branch = mapping.num_branch
            value_mapping = mapping.value_source
            dataset_source = self.metadata_to_load.get_dataset_from_dataset_name(
                self.metadata_actual.get_table_name_from_cod_entity_on_entry(mapping.cod_entity_source))

            # TODO: Search source tables from ENTRY_DATASET_MAPPINGS to be able to accept different columns from diferent tables on only one mapping.
            all_columns_from_source = self.metadata_to_load.get_all_columns_from_table_name(
                self.metadata_actual.get_table_name_from_cod_entity_on_entry(mapping.cod_entity_source))
            for col in all_columns_from_source:
                if re.search(r"\s+|\(," + col + "\s+|\)|,", value_mapping) or re.search(r"(^" + col + "$)",
                                                                                        value_mapping):
                    dataset_spec_source = self.metadata_to_load.get_dataset_spec_from_id_dataset_and_column_name(
                        dataset_source.id_dataset, col)
                    value_mapping = re.sub(col, "[" + str(dataset_spec_source.id_dataset_spec) + "]", value_mapping)

            dataset_t_mapping = self.metadata_actual.get_dataset_t_mapping_from_id_branch_and_id_dataset_spec_and_value_mapping(
                id_branch, dataset_spec.id_dataset_spec, value_mapping)

            if dataset_t_mapping is None:
                id_t_mapping = next_id_t_mapping
                next_id_t_mapping += 1
                new_dataset_t_mapping = [id_t_mapping, id_branch, dataset_spec.id_dataset_spec, value_mapping,
                                         self.owner, self.connection_metadata.get_sysdate_value(), "NULL"]
                self.metadata_to_load.add_om_dataset_t_mapping([new_dataset_t_mapping])
                mapping_loaded.append([id_branch, dataset_spec.id_dataset_spec, value_mapping])

            else:
                if value_mapping == dataset_t_mapping.value_mapping:
                    existent_mapping = [dataset_t_mapping.id_t_mapping, dataset_t_mapping.id_branch,
                                        dataset_t_mapping.id_dataset_spec, dataset_t_mapping.value_mapping,
                                        dataset_t_mapping.meta_owner, "'" + str(dataset_t_mapping.start_date) + "'",
                                        "NULL"]
                    self.metadata_to_load.add_om_dataset_t_mapping([existent_mapping])
                    mapping_loaded.append([dataset_t_mapping.id_branch, dataset_t_mapping.id_dataset_spec,
                                           dataset_t_mapping.value_mapping])
                else:
                    existent_mapping = [dataset_t_mapping.id_t_mapping, dataset_t_mapping.id_branch,
                                        dataset_t_mapping.id_dataset_spec, dataset_t_mapping.value_mapping,
                                        dataset_t_mapping.meta_owner, "'" + str(dataset_t_mapping.start_date) + "'",
                                        self.connection_metadata.get_sysdate_value()]
                    self.metadata_to_load.add_om_dataset_t_mapping([existent_mapping])
                    mapping_loaded.append([dataset_t_mapping.id_branch, dataset_t_mapping.id_dataset_spec,
                                           dataset_t_mapping.value_mapping])

                    id_t_mapping = next_id_t_mapping
                    next_id_t_mapping += 1
                    new_dataset_t_mapping = [id_t_mapping, id_branch, dataset_spec.id_dataset_spec, value_mapping,
                                             self.owner, self.connection_metadata.get_sysdate_value(), "NULL"]
                    self.metadata_to_load.add_om_dataset_t_mapping([new_dataset_t_mapping])
                    mapping_loaded.append([id_branch, dataset_spec.id_dataset_spec, value_mapping])

        for mapping in [x for x in self.metadata_actual.om_dataset_t_mapping if x.end_date is None]:
            if [mapping.id_branch, mapping.id_dataset_spec, mapping.value_mapping] not in mapping_loaded:
                close_mapping = [mapping.id_t_mapping, mapping.id_branch,
                                 mapping.id_dataset_spec, mapping.value_mapping,
                                 mapping.meta_owner, "'" + str(mapping.start_date) + "'",
                                 self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_t_mapping([close_mapping])

    def process_elt_filter(self):
        next_id_t_filter = self.next_id_t_filter
        ######################## LOAD FILTER ########################
        filter_loaded = []
        for filter in self.metadata_actual.entry_filters:
            dataset = self.metadata_to_load.get_dataset_from_dataset_name(self.metadata_actual.get_table_name_from_cod_entity_on_entry(filter.cod_entity_target))
            id_branch = filter.num_branch
            value_mapping = filter.value

            all_source_tables = self.metadata_to_load.get_all_source_tables_from_target_table_name(self.metadata_actual.get_table_name_from_cod_entity_on_entry(filter.cod_entity_target))
            for source in all_source_tables:
                dataset_source = self.metadata_to_load.get_dataset_from_dataset_name(source)
                all_columns_from_source = self.metadata_to_load.get_all_columns_from_table_name(
                    dataset_source.dataset_name)
                for col in all_columns_from_source:
                    if re.search(r"\s+|\(," + col + "\s+|\)|,", value_mapping) or re.search(r"(^" + col + "$)",
                                                                                            value_mapping):
                        dataset_spec_source = self.metadata_to_load.get_dataset_spec_from_id_dataset_and_column_name(
                            dataset_source.id_dataset, col)
                        value_mapping = re.sub(col, "[" + str(dataset_spec_source.id_dataset_spec) + "]", value_mapping)

            dataset_t_filter = self.metadata_actual.get_dataset_t_filter_from_id_dataset_and_id_branch_and_value_filter(dataset.id_dataset, id_branch, value_mapping)
            if dataset_t_filter is None:
                id_t_filter = next_id_t_filter
                next_id_t_filter += 1
                new_dataset_t_filter = [id_t_filter, dataset.id_dataset, id_branch, value_mapping, self.owner,
                                        self.connection_metadata.get_sysdate_value(), "NULL"]
                self.metadata_to_load.add_om_dataset_t_filter([new_dataset_t_filter])
                filter_loaded.append([dataset.id_dataset, id_branch, value_mapping])

            else:
                if value_mapping == dataset_t_filter.value_filter:
                    existent_filter = [dataset_t_filter.id_t_filter, dataset_t_filter.id_dataset,
                                       dataset_t_filter.id_branch,
                                       dataset_t_filter.value_filter, dataset_t_filter.meta_owner,
                                       "'" + str(dataset_t_filter.start_date) + "'", "NULL"]
                    self.metadata_to_load.add_om_dataset_t_filter([existent_filter])
                    filter_loaded.append(
                        [dataset_t_filter.id_dataset, dataset_t_filter.id_branch, dataset_t_filter.value_filter])
                else:
                    existent_filter = [dataset_t_filter.id_t_filter, dataset_t_filter.id_dataset,
                                       dataset_t_filter.id_branch,
                                       dataset_t_filter.value_filter, dataset_t_filter.meta_owner,
                                       "'" + str(dataset_t_filter.start_date) + "'",
                                       self.connection_metadata.get_sysdate_value()]
                    self.metadata_to_load.add_om_dataset_t_filter([existent_filter])
                    filter_loaded.append([dataset_t_filter.id_dataset, dataset_t_filter.id_branch, dataset_t_filter.value_filter])

                    id_t_filter = next_id_t_filter
                    next_id_t_filter += 1
                    new_dataset_t_filter = [id_t_filter, dataset.id_dataset, id_branch, value_mapping, self.owner,
                                            self.connection_metadata.get_sysdate_value(), "NULL"]
                    self.metadata_to_load.add_om_dataset_t_filter([new_dataset_t_filter])
                    filter_loaded.append([dataset.id_dataset, id_branch, value_mapping])


        for filter in [x for x in self.metadata_actual.om_dataset_t_filter if x.end_date is None]:
            if [filter.id_dataset, filter.id_branch, filter.value_filter] not in filter_loaded:
                close_filter = [filter.id_t_filter, filter.id_dataset,
                                filter.id_branch,
                                filter.value_filter, filter.meta_owner,
                                "'" + str(filter.start_date) + "'", self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_t_filter([close_filter])

    def process_elt_having(self):
        next_id_t_having = self.next_id_t_having
        ######################## LOAD HAVING ########################
        having_loaded = []
        for having in self.metadata_actual.entry_having:
            dataset = self.metadata_to_load.get_dataset_from_dataset_name(self.metadata_actual.get_table_name_from_cod_entity_on_entry(having.cod_entity_target))
            id_branch = having.num_branch
            value_having = having.value

            all_source_tables = self.metadata_to_load.get_all_source_tables_from_target_table_name(
                self.metadata_actual.get_table_name_from_cod_entity_on_entry(having.cod_entity_target))
            for source in all_source_tables:
                dataset_source = self.metadata_to_load.get_dataset_from_dataset_name(source)
                all_columns_from_source = self.metadata_to_load.get_all_columns_from_table_name(
                    dataset_source.dataset_name)
                for col in all_columns_from_source:
                    if re.search(r"\s+|\(," + col + "\s+|\)|,", value_having) or re.search(r"(^" + col + "$)", value_having):
                        dataset_spec_source = self.metadata_to_load.get_dataset_spec_from_id_dataset_and_column_name(
                            dataset_source.id_dataset, col)
                        value_having = re.sub(col, "[" + str(dataset_spec_source.id_dataset_spec) + "]", value_having)

            dataset_t_having = self.metadata_actual.get_dataset_t_having_from_id_dataset_and_id_branch_and_value_having(
                dataset.id_dataset, id_branch, value_having)

            if dataset_t_having is None:
                id_t_having = next_id_t_having
                next_id_t_having += 1
                new_dataset_t_having = [id_t_having, dataset.id_dataset, id_branch, value_having, self.owner,
                                        self.connection_metadata.get_sysdate_value(), "NULL"]
                self.metadata_to_load.add_om_dataset_t_having([new_dataset_t_having])
                having_loaded.append([dataset.id_dataset, id_branch, value_having])

            else:
                if value_having == dataset_t_having.value_having:
                    existent_having = [dataset_t_having.id_t_having, dataset_t_having.id_dataset,
                                       dataset_t_having.id_branch,
                                       dataset_t_having.value_having, dataset_t_having.meta_owner,
                                       "'" + str(dataset_t_having.start_date) + "'", "NULL"]
                    self.metadata_to_load.add_om_dataset_t_having([existent_having])
                    having_loaded.append(
                        [dataset_t_having.id_dataset, dataset_t_having.id_branch, dataset_t_having.value_having])
                else:
                    existent_having = [dataset_t_having.id_t_having, dataset_t_having.id_dataset,
                                       dataset_t_having.id_branch,
                                       dataset_t_having.value_having, dataset_t_having.meta_owner,
                                       "'" + str(dataset_t_having.start_date) + "'",
                                       self.connection_metadata.get_sysdate_value()]
                    self.metadata_to_load.add_om_dataset_t_having([existent_having])
                    having_loaded.append(
                        [dataset_t_having.id_dataset, dataset_t_having.id_branch, dataset_t_having.value_having])

                    id_t_having = next_id_t_having
                    next_id_t_having += 1
                    new_dataset_t_having = [id_t_having, dataset.id_dataset, id_branch, value_having,
                                            self.owner, self.connection_metadata.get_sysdate_value(), "NULL"]
                    self.metadata_to_load.add_om_dataset_t_having([new_dataset_t_having])
                    having_loaded.append([dataset.id_dataset, id_branch, value_having])

        for having in [x for x in self.metadata_actual.om_dataset_t_having if x.end_date is None]:
            if [having.id_dataset, having.id_branch, having.value_having] not in having_loaded:
                close_having = [having.id_t_having, having.id_dataset,
                                having.id_branch,
                                having.value_having, having.meta_owner,
                                "'" + str(having.start_date) + "'", self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_t_having([close_having])

    def process_elt_historical(self):
        ######################## LOAD HISTORIC METADATA ########################
        for path in [x for x in self.metadata_actual.om_dataset_path if x.end_date is not None]:
            close_path = [path.id_path, path.database_name, path.schema_name, path.meta_owner,
                          "'" + str(path.start_date) + "'", "'" + str(path.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_path([close_path])

        for source in [x for x in self.metadata_actual.om_dataset if x.end_date is not None]:
            close_source = [source.id_dataset, source.dataset_name, source.id_entity_type,
                            source.id_path, source.meta_owner, "'" + str(source.start_date) + "'",
                            "'" + str(source.end_date) + "'"]
            self.metadata_to_load.add_om_dataset([close_source])

        for closed_col in [x for x in self.metadata_actual.om_dataset_specification if x.end_date is not None]:
            self.metadata_to_load.add_om_dataset_specification([[closed_col.id_dataset_spec, closed_col.id_dataset,
                                                                 closed_col.id_key_type, closed_col.column_name,
                                                                 closed_col.column_type,
                                                                 closed_col.ordinal_position, closed_col.is_nullable,
                                                                 closed_col.length,
                                                                 closed_col.precision, closed_col.scale,
                                                                 closed_col.meta_owner,
                                                                 "'" + str(closed_col.start_date) + "'",
                                                                 "'" + str(closed_col.end_date) + "'"]])

        for order_type in [x for x in self.metadata_actual.om_dataset_t_order if x.end_date is not None]:
            close_order = [order_type.id_t_order, order_type.id_dataset, order_type.id_branch,
                           order_type.id_dataset_spec,
                           order_type.id_order_type, order_type.meta_owner, "'" + str(order_type.start_date) + "'",
                           "'" + str(order_type.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_t_order([close_order])

        for relationship in [x for x in self.metadata_actual.om_dataset_relationships if x.end_date is not None]:
            old_relationship = [relationship.id_relationship,
                                relationship.id_dataset_spec_master,
                                relationship.id_dataset_spec_detail,
                                relationship.id_join_type, relationship.meta_owner,
                                "'" + str(relationship.start_date) + "'", "'" + str(relationship.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_relationships([old_relationship])

        for agg in [x for x in self.metadata_actual.om_dataset_t_agg if x.end_date is not None]:
            new_agg = [agg.id_t_agg, agg.id_dataset, agg.id_branch,
                       agg.id_dataset_spec,
                       agg.meta_owner, "'" + str(agg.start_date) + "'", "'" + str(agg.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_t_agg([new_agg])

        for distinct in [x for x in self.metadata_actual.om_dataset_t_distinct if x.end_date is not None]:
            close_distinct = [distinct.id_t_distinct, distinct.id_dataset, distinct.id_branch, distinct.sw_distinct
                , distinct.meta_owner, "'" + distinct.start_date + "'", "'" + str(distinct.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_t_distinct([close_distinct])

        for mapping in [x for x in self.metadata_actual.om_dataset_t_mapping if x.end_date is not None]:
            close_mapping = [mapping.id_t_mapping, mapping.id_branch,
                             mapping.id_dataset_spec, mapping.value_mapping,
                             mapping.meta_owner, "'" + mapping.start_date + "'", "'" + str(mapping.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_t_mapping([close_mapping])

        for filter in [x for x in self.metadata_actual.om_dataset_t_filter if x.end_date is not None]:
            close_filter = [filter.id_t_filter, filter.id_dataset,
                            filter.id_branch,
                            filter.value_filter, filter.meta_owner,
                            "'" + filter.start_date + "'", "'" + str(filter.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_t_filter([close_filter])

        for having in [x for x in self.metadata_actual.om_dataset_t_having if x.end_date is not None]:
            close_having = [having.id_t_having, having.id_dataset,
                            having.id_branch,
                            having.value_having, having.meta_owner,
                            "'" + having.start_date + "'", "'" + str(having.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_t_having([close_having])

        for execution in [x for x in self.metadata_actual.om_dataset_execution if x.end_date is not None]:

            close_execution = [execution.id_dataset, execution.id_query_type, execution.meta_owner,
                               "'" +str(execution.start_date)+ "'", "'" +str(execution.end_date)+ "'"]
            self.metadata_to_load.add_om_dataset_execution([close_execution])

    def process_dv(self):
        self.log.log(self.engine_name, "Starting to process Metadata from DV Module", LOG_LEVEL_INFO)

        self.log.log(self.engine_name, "Under development. It is recommended to disable DV module.", LOG_LEVEL_ERROR)

        self.log.log(self.engine_name, "Finished to process Metadata from DV Module", LOG_LEVEL_INFO)


    def upload_metadata(self):
        self.log.log(self.engine_name, "Starting to upload all the metadata processed", LOG_LEVEL_INFO)

        connection_type = self.configuration_file['metadata']['connection_type']
        connection = ConnectionFactory().get_connection(connection_type)
        connection.setup_connection(self.configuration_file['metadata'], self.log)
        where_filter_owner = "META_OWNER='" + self.owner + "'"
        commit_values_batch = self.properties_file['options']['max_commit_batch']

        # OM_DATASET_PATH
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_PATH)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_PATH)
        query.set_insert_columns(COLUMNS_OM_DATASET_PATH)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_path)
        connection.execute(str(query))

        # OM_DATASET
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET)
        query.set_insert_columns(COLUMNS_OM_DATASET)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset)
        connection.execute(str(query))

        # OM_DATASET_SPECIFICATION
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_SPECIFICATION)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_SPECIFICATION)
        query.set_insert_columns(COLUMNS_OM_DATASET_SPECIFICATION)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_specification)
        connection.execute(str(query))

        # OM_DATASET_RELATIONSHIPS
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_RELATIONSHIPS)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_RELATIONSHIPS)
        query.set_insert_columns(COLUMNS_OM_DATASET_RELATIONSHIPS)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_relationships)
        connection.execute(str(query))

        # OM_DATASET_T_AGG
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_T_AGG)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_T_AGG)
        query.set_insert_columns(COLUMNS_OM_DATASET_T_AGG)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_t_agg)
        connection.execute(str(query))

        # OM_DATASET_T_ORDER
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_T_ORDER)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_T_ORDER)
        query.set_insert_columns(COLUMNS_OM_DATASET_T_ORDER)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_t_order)
        connection.execute(str(query))

        # OM_DATASET_T_MAPPING
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_T_MAPPING)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_T_MAPPING)
        query.set_insert_columns(COLUMNS_OM_DATASET_T_MAPPING)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_t_mapping)
        connection.execute(str(query))

        # OM_DATASET_T_DISTINCT
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_T_DISTINCT)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_T_DISTINCT)
        query.set_insert_columns(COLUMNS_OM_DATASET_T_DISTINCT)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_t_distinct)
        connection.execute(str(query))

        # OM_DATASET_T_FILTER
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_T_FILTER)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_T_FILTER)
        query.set_insert_columns(COLUMNS_OM_DATASET_T_FILTER)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_t_filter)
        connection.execute(str(query))

        # OM_DATASET_T_HAVING
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_T_HAVING)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_T_HAVING)
        query.set_insert_columns(COLUMNS_OM_DATASET_T_HAVING)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_t_having)
        connection.execute(str(query))

        # OM_DATASET_EXECUTION
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_EXECUTION)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_EXECUTION)
        query.set_insert_columns(COLUMNS_OM_DATASET_EXECUTION)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_execution)
        connection.execute(str(query))

        connection.commit()
        connection.close()

        self.log.log(self.engine_name, "Uploading completed", LOG_LEVEL_INFO)
