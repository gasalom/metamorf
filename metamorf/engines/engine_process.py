from metamorf.engines.engine import Engine
from metamorf.tools.connection import ConnectionFactory
from metamorf.constants import *
from metamorf.tools.metadata import Metadata
import re
from metamorf.tools.query import Query
from metamorf.tools.metadata_validator import MetadataValidator

class EngineProcess(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Process"
        self.engine_command = "process"
        self.module_elt_active = False
        self.module_dv_active = False
        self.module_dv_char_separator_naming = "_"

    def run(self):
        # Starts the execution loading the Configuration File. If there is an error it finishes the execution.
        super().start_execution()

        if len(self.modules_to_execute) == 0:
            self.log.log(self.engine_name, "No Modules are Active - No metadata will be processed", LOG_LEVEL_WARNING)
            super().finish_execution(False)
            return

        self.connection = ConnectionFactory().get_connection(self.configuration_file['data']['connection_type'])
        self.connection_metadata = ConnectionFactory().get_connection(self.configuration_file['metadata']['connection_type'])
        self.metadata_actual = self.load_metadata(load_om=True, load_entry=True, load_ref=True, load_im=False, owner=self.owner)
        self.metadata_to_load = Metadata(self.log)

        metadata_validator = MetadataValidator(self.metadata_actual, self.connection, self.configuration_file, self.log)
        result_validation_metadata_entry = metadata_validator.validate_metadata()
        if result_validation_metadata_entry == False:
            self.log.log(self.engine_name, "Metadata Entry Validation has not passed. Please review the errors.", LOG_LEVEL_CRITICAL)
            super().finish_execution(False)
            return
        else:
            self.log.log(self.engine_name, "Metadata Entry validation - Ok", LOG_LEVEL_OK)

        # If there's nothing to load it finishes the execution
        if len(self.metadata_actual.entry_entity)==0:
            self.log.log(self.engine_name, "There are no entities loaded, some datasets might be decommissioned", LOG_LEVEL_WARNING)

        self.get_next_ids()

        # Process Metadata and get new Metadata to update database
        if MODULE_DV in self.modules_to_execute or MODULE_ELT in self.modules_to_execute: self.process_common()

        if MODULE_DV in self.modules_to_execute: self.process_dv()
        if MODULE_ELT in self.modules_to_execute: self.process_elt()
        if MODULE_DV in self.modules_to_execute: self.process_dv_final()


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
        self.log.log(self.engine_name, "Starting to get id's from database", LOG_LEVEL_ONLY_LOG)
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
        self.log.log(self.engine_name, "Finished to get id's from database", LOG_LEVEL_ONLY_LOG)

    def process_common(self):
        self.log.log(self.engine_name, "Starting to process Metadata from all modules", LOG_LEVEL_INFO)
        self.process_elt_path()
        self.log.log(self.engine_name, "Finished to process Metadata from all modules", LOG_LEVEL_INFO)

    def process_elt(self):
        self.log.log(self.engine_name, "Starting to process Metadata from ELT Module", LOG_LEVEL_INFO)

        self.process_elt_sources()
        self.process_elt_execution()
        self.process_elt_files()
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
        self.log.log(self.engine_name, "Starting to process Metadata [ Path ] information", LOG_LEVEL_ONLY_LOG)

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

        self.log.log(self.engine_name, "Finished to process Metadata [ Path ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_execution(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Execution ] information", LOG_LEVEL_ONLY_LOG)

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

        self.log.log(self.engine_name, "Finished to process Metadata [ Execution ] information", LOG_LEVEL_ONLY_LOG)

    def get_hash_key_from_cod_entity_target_and_num_branch(self, hub, num_branch):
        has_tn = False
        has_seq = False
        tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(hub, num_branch)
        if len(tenant_source) != 0:
            has_tn = True
            tenant_source.sort(key=lambda x: x.ordinal_position)

        seq_source = self.metadata_actual.get_seq_on_dv_from_cod_entity_target_and_num_branch(hub, num_branch)
        if len(seq_source) != 0:
            has_seq = True
            seq_source.sort(key=lambda x: x.ordinal_position)

        entry_dv_mapping_bk = self.metadata_actual.get_all_bk_from_entry_dv_cod_entity_target_and_num_branch(hub, num_branch)
        entry_dv_mapping_bk.sort(key=lambda x: x.ordinal_position)

        md5_function = self.connection.get_md5_function()

        cast_to_string = self.connection.get_cast_string_for_metadata()

        bk_concatenate = ''
        for bk in entry_dv_mapping_bk:
            bk_final = cast_to_string.replace('[x]', self.connection.get_if_is_null().replace('[x]', bk.column_name_source))
            bk_concatenate += bk_final + "||'" + self.module_dv_char_separator_naming + "'||"
        bk_concatenate = bk_concatenate[:-(len(self.module_dv_char_separator_naming) + 6)]

        tenant_concatenate = ''
        for tn in tenant_source:
            tn_final = cast_to_string.replace('[x]', tn.column_name_source)
            tenant_concatenate += tn_final + "||'" + self.module_dv_char_separator_naming + "'||"
        tenant_concatenate = tenant_concatenate[:-(len(self.module_dv_char_separator_naming) + 6)]

        seq_concatenate = ''
        for seq in seq_source:
            seq_final=cast_to_string.replace('[x]', seq.column_name_source)
            seq_concatenate+=seq_final + "||'" + self.module_dv_char_separator_naming + "'||"
        seq_concatenate = seq_concatenate[:-(len(self.module_dv_char_separator_naming) + 6)]

        md5_concatenate = ''
        separator = "||'" + self.module_dv_char_separator_naming + "'||"
        if has_tn and has_seq:
            md5_concatenate = bk_concatenate + separator + tenant_concatenate + separator + seq_concatenate
        elif has_tn and not has_seq:
            md5_concatenate = bk_concatenate + separator + tenant_concatenate
        elif has_seq and not has_tn:
            md5_concatenate = bk_concatenate + separator + seq_concatenate
        else:
            md5_concatenate = bk_concatenate

        md5_function = md5_function.replace('[x]', md5_concatenate)
        return md5_function

    def get_hash_key_from_cod_entity_target_and_num_branch_and_num_connection(self, link, num_branch, num_connection):
        has_tn = False
        tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch_and_num_connection(link, num_branch, num_connection)
        if len(tenant_source) != 0:
            has_tn = True
            tenant_source.sort(key=lambda x: x.ordinal_position)

        entry_dv_mapping_bk = self.metadata_actual.get_all_bk_from_entry_dv_cod_entity_target_and_num_branch_and_num_connection(link, num_branch, num_connection)
        entry_dv_mapping_bk.sort(key=lambda x: x.ordinal_position)

        md5_function = self.connection.get_md5_function()
        cast_to_string = self.connection.get_cast_string_for_metadata()

        bk_concatenate = ''
        for bk in entry_dv_mapping_bk:
            bk_final = cast_to_string.replace('[x]', bk.column_name_source)
            bk_concatenate += bk_final + "||'" + self.module_dv_char_separator_naming + "'||"

        tenant_concatenate = ''
        for tn in tenant_source:
            tn_final = cast_to_string.replace('[x]', tn.column_name_source)
            tenant_concatenate += tn_final + "||'" + self.module_dv_char_separator_naming + "'||"
        tenant_concatenate = tenant_concatenate[:-(len(self.module_dv_char_separator_naming) + 6)]

        if has_tn:
            bk_concatenate += tenant_concatenate
        else:
            bk_concatenate = bk_concatenate[:-(len(self.module_dv_char_separator_naming) + 6)]
        md5_function = md5_function.replace('[x]', bk_concatenate)
        return md5_function

    def process_dv_hub_creation_hub(self, hub):
        self.log.log(self.engine_name, "Starting to process Metadata [ Hub definition ] information", LOG_LEVEL_ONLY_LOG)
        ############################################################################################################
        prefix_et = 'ET_'

        # Creation of HUB ENTITY
        ordinal_position = 1
        has_rs = False
        has_tn = False
        has_ad = False
        hub_stg_tmp_name = 'STG_TMP_' + hub.entity_name
        hub_stg_name = 'STG_' + hub.entity_name
        hub_stg_name_last_image = 'STG_' + hub.entity_name + '_LAST_IMAGE'
        hub_name = hub.entity_name

        hash_name = 'HASH_' + hub.entity_name
        dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(hub.cod_entity, 0)
        if dv_property is not None: hash_name = dv_property.hash_name

        new_entity_stg_tmp = [prefix_et + hub_stg_tmp_name, hub_stg_tmp_name, ENTITY_WITH, hub.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_stg_tmp])
        new_entity_stg = [prefix_et + hub_stg_name, hub_stg_name, ENTITY_WITH, hub.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_stg])
        new_entity_hub = [prefix_et + hub_stg_name_last_image, hub_stg_name_last_image, ENTITY_WITH, hub.cod_path, "", self.owner]
        self.metadata_actual.add_entry_entity([new_entity_hub])
        new_entity_hub = [prefix_et + hub_name, hub_name, ENTITY_TB, hub.cod_path, "INSERT", self.owner]
        self.metadata_actual.add_entry_entity([new_entity_hub])

        # Include ENTRY from ET_STG_TMP_[Hub]
        entry_dv_mapping_bk = []
        record_source = None
        tenant_source = None
        applied_date = None
        num_branches = self.metadata_actual.get_num_branches_on_entry_dv_from_cod_entity_name(hub.cod_entity)
        for num_branch in range(1, num_branches + 1):
            entry_dv_mapping_bk = self.metadata_actual.get_all_bk_from_entry_dv_cod_entity_target_and_num_branch(hub.cod_entity, num_branch)
            entry_dv_mapping_bk.sort(key=lambda x: x.ordinal_position)
            cod_entity_source = entry_dv_mapping_bk[0].cod_entity_source

            tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(hub.cod_entity, num_branch)
            if len(tenant_source) != 0: has_tn = True
            record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(hub.cod_entity, num_branch)
            if record_source is not None: has_rs = True
            applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(hub.cod_entity, num_branch)
            if applied_date is not None: has_ad = True


            md5_function = self.get_hash_key_from_cod_entity_target_and_num_branch(hub.cod_entity, num_branch)

            hash_for_metadata = self.connection.get_hash_for_metadata()
            new_dataset_mapping = [cod_entity_source, md5_function, prefix_et + hub_stg_tmp_name,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + hub_stg_tmp_name,
                                   'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], num_branch, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [record_source.cod_entity_source, record_source.column_name_source,
                                       prefix_et + hub_stg_tmp_name,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_ad:
                new_dataset_mapping = [applied_date.cod_entity_source, applied_date.column_name_source,
                                       prefix_et + hub_stg_tmp_name,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                       applied_date.column_precision,
                                       num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                for tn in tenant_source:
                    new_dataset_mapping = [tn.cod_entity_source, tn.column_name_source, prefix_et + hub_stg_tmp_name,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length, tn.column_precision,
                                           num_branch, None, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            for bk in entry_dv_mapping_bk:
                new_dataset_mapping = [cod_entity_source, bk.column_name_source, prefix_et + hub_stg_tmp_name,
                                       bk.column_name_target,
                                       bk.column_type_target, ordinal_position + int(bk.ordinal_position), bk.column_length,
                                       bk.column_precision,
                                       num_branch, KEY_TYPE_BUSINESS_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        # Relationship on STG_TMP and HUB
        ordinal_position = 1
        new_relationship = [prefix_et + hub_stg_tmp_name, hash_name, prefix_et + hub_name,
                            hash_name, 'MASTER JOIN', self.owner]
        self.metadata_actual.add_entry_dataset_relationship([new_relationship])

        # STG
        hash_for_metadata = self.connection.get_hash_for_metadata()
        new_dataset_mapping = [prefix_et + hub_stg_tmp_name, hash_name, prefix_et + hub_stg_name,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2], 1,
                               KEY_TYPE_HASH_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        new_dataset_mapping = [prefix_et + hub_name, hash_name, prefix_et + hub_stg_name,
                               hash_name + "_HUB",
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2], 1,
                               KEY_TYPE_HASH_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = [prefix_et + hub_stg_tmp_name, 'DATE_CREATED', prefix_et + hub_stg_name, 'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], 1, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        for bk in entry_dv_mapping_bk:
            new_dataset_mapping = [prefix_et + hub_stg_tmp_name, bk.column_name_target, prefix_et + hub_stg_name,
                                   bk.column_name_target,
                                   bk.column_type_target, ordinal_position + int(bk.ordinal_position), bk.column_length,
                                   bk.column_precision,
                                   1, KEY_TYPE_BUSINESS_KEY, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [prefix_et + hub_stg_tmp_name, record_source.column_name_target,
                                   prefix_et + hub_stg_name,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + hub_stg_tmp_name, tn.column_name_target, prefix_et + hub_stg_name,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [prefix_et + hub_stg_tmp_name, applied_date.column_name_target,
                                   prefix_et + hub_stg_name,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        ################################## Get new business keys ##################################
        # Filter
        new_filter = [prefix_et + hub_stg_name_last_image, hash_name + "_HUB is null", 1, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        ordinal_position = 1
        hash_for_metadata = self.connection.get_hash_for_metadata()
        new_dataset_mapping = [prefix_et + hub_stg_name, hash_name, prefix_et + hub_stg_name_last_image,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2], 1,
                               KEY_TYPE_HASH_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = [prefix_et + hub_stg_name, 'DATE_CREATED', prefix_et + hub_stg_name_last_image, 'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], 1, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [prefix_et + hub_stg_name, record_source.column_name_target, prefix_et + hub_stg_name_last_image,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        if has_ad:
            new_dataset_mapping = [prefix_et + hub_stg_name, applied_date.column_name_target, prefix_et + hub_stg_name_last_image,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + hub_stg_name, tn.column_name_target, prefix_et + hub_stg_name_last_image,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        entry_dv_mapping_bk.sort(key=lambda x: x.ordinal_position)
        for bk in entry_dv_mapping_bk:
            new_dataset_mapping = [prefix_et + hub_stg_name, bk.column_name_target, prefix_et + hub_stg_name_last_image,
                                   bk.column_name_target,
                                   bk.column_type_target, ordinal_position, bk.column_length,
                                   bk.column_precision,
                                   1, KEY_TYPE_BUSINESS_KEY, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        integer_for_metadata = self.connection.get_integer_for_metadata()
        date_for_last_image = 'DATE_CREATED'
        if has_ad: date_for_last_image = applied_date.column_name_target
        new_dataset_mapping = [prefix_et + hub_stg_name,
                               'ROW_NUMBER() over (partition by ' + hash_name + ' ORDER BY ' + date_for_last_image + ' desc)',
                               prefix_et + hub_stg_name_last_image, 'RN',
                               integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                               integer_for_metadata[2],
                               1, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1


        ############################# Final Hub #################################
        ordinal_position = 1
        hash_for_metadata = self.connection.get_hash_for_metadata()
        new_dataset_mapping = [prefix_et + hub_stg_name_last_image, hash_name, prefix_et + hub_name,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2], 1,
                               KEY_TYPE_HASH_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = [prefix_et + hub_stg_name_last_image, 'DATE_CREATED',
                               prefix_et + hub_name,
                               'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], 1, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [prefix_et + hub_stg_name_last_image, record_source.column_name_target,
                                   prefix_et + hub_name,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        if has_ad:
            new_dataset_mapping = [prefix_et + hub_stg_name_last_image, applied_date.column_name_target,
                                   prefix_et + hub_name,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + hub_stg_name_last_image, tn.column_name_target,
                                       prefix_et + hub_name,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        entry_dv_mapping_bk.sort(key=lambda x: x.ordinal_position)
        for bk in entry_dv_mapping_bk:
            new_dataset_mapping = [prefix_et + hub_stg_name_last_image, bk.column_name_target,
                                   prefix_et + hub_name,
                                   bk.column_name_target,
                                   bk.column_type_target, ordinal_position, bk.column_length,
                                   bk.column_precision,
                                   1, KEY_TYPE_BUSINESS_KEY, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        new_filter = [prefix_et + hub_name, "RN = 1", 1, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        self.log.log(self.engine_name, "Finished to process Metadata [ Hub definition ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_hub_creation_sat(self, hub):
        self.log.log(self.engine_name, "Starting to process Metadata [ Hub satellites ] information", LOG_LEVEL_ONLY_LOG)

        all_satellites = self.metadata_actual.get_all_satellites_info_from_hub(hub.cod_entity)
        # SAT: cod_entity_source | cod_entity_target | satellite_name | num_branch | origin_is_incremental | origin_is_total | origin_is_cdc
        for sat in all_satellites:
            if int(sat[6]) == 0: self.process_dv_hub_creation_sat_non_cdc(hub, sat)
            elif int(sat[6]) == 1: self.process_dv_hub_creation_sat_cdc(hub, sat)

        self.log.log(self.engine_name, "Finished to process Metadata [ Hub satellites ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_hub_creation_sat_non_cdc(self, hub, sat):
        self.log.log(self.engine_name, "Starting to process Metadata [ Hub satellites - non cdc ] information", LOG_LEVEL_ONLY_LOG)
        ordinal_position = 1
        prefix_et = 'ET_'
        sat_cod_entity_source = sat[0]
        sat_cod_entity_target = sat[1]
        sat_name = sat[2]
        sat_num_branch = 1 # Sat can't have more than one branch -> sat[3]

        hash_name = 'HASH_' + hub.entity_name

        dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(hub.cod_entity, 0)
        if dv_property is not None: hash_name = dv_property.hash_name

        ########################### Create all entities ###########################
        sat_entity_tmp = 'STG_TMP_' + sat_name
        sat_entity_actual_image_1 = 'STG_TMP_LAST_IMAGE_1_' + sat_name
        sat_entity_actual_image_2 = 'STG_TMP_LAST_IMAGE_2_' + sat_name
        sat_entity_join = 'STG_TMP_JOIN_' + sat_name
        sat_entity = sat_name

        new_entity_sat_entity_tmp = [prefix_et + sat_entity_tmp, sat_entity_tmp, ENTITY_WITH, hub.cod_path, '',
                                     self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_tmp])
        new_entity_sat_entity_actual_image_1 = [prefix_et + sat_entity_actual_image_1, sat_entity_actual_image_1,
                                                ENTITY_WITH, hub.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_actual_image_1])
        new_entity_sat_entity_actual_image_2 = [prefix_et + sat_entity_actual_image_2, sat_entity_actual_image_2,
                                                ENTITY_WITH, hub.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_actual_image_2])
        new_entity_sat_entity_join = [prefix_et + sat_entity_join, sat_entity_join, ENTITY_WITH, hub.cod_path, '',
                                      self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_join])
        new_entity_sat_entity = [prefix_et + sat_entity, sat_entity, ENTITY_TB, hub.cod_path, 'INSERT', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity])

        has_rs = False
        has_tn = False
        has_dck = False
        has_ad = False
        tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat_num_branch)
        if len(tenant_source) != 0: has_tn = True
        record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat_num_branch)
        if record_source is not None: has_rs = True
        dependent_child_key = self.metadata_actual.get_dependent_child_key_on_dv_from_satellite_name(sat_name)
        if len(dependent_child_key) != 0: has_dck = True
        applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(hub.cod_entity, sat[3])
        if applied_date is not None: has_ad = True

        hash_for_metadata = self.connection.get_hash_for_metadata()
        integer_for_metadata = self.connection.get_integer_for_metadata()

        ########################### Create Entity STG TMP ###########################
        md5_function = self.get_hash_key_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat[3])
        hash_md5_function = md5_function
        new_dataset_mapping = [sat_cod_entity_source, md5_function, prefix_et + sat_entity_tmp,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + sat_entity_tmp,
                               'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [sat_cod_entity_source, record_source.column_name_source,
                                   prefix_et + sat_entity_tmp,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   sat_num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [sat_cod_entity_source, applied_date.column_name_source,
                                   prefix_et + sat_entity_tmp,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   sat_num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [sat_cod_entity_source, tn.column_name_source, prefix_et + sat_entity_tmp,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        all_dck_concatenate = ''
        if has_dck:
            for dck in dependent_child_key:
                all_dck_concatenate += ", " + dck.column_name_source
                new_dataset_mapping = [sat_cod_entity_source, dck.column_name_source, prefix_et + sat_entity_tmp,
                                       dck.column_name_target,
                                       dck.column_type_target, ordinal_position, dck.column_length,
                                       dck.column_precision,
                                       1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        all_attributes = self.metadata_actual.get_attributes_on_dv_from_satellite_name(sat_entity)

        for at in all_attributes:
            new_dataset_mapping = [at.cod_entity_source, at.column_name_source,
                                   prefix_et + sat_entity_tmp,
                                   at.column_name_target,
                                   at.column_type_target, ordinal_position, at.column_length,
                                   at.column_precision,
                                   sat_num_branch, at.key_type, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        md5_function = self.connection.get_md5_function()
        cast_to_string = self.connection.get_cast_string_for_metadata()

        bk_concatenate = ''
        at_cod_entity_source = ''
        for at in all_attributes:
            bk_final = cast_to_string.replace('[x]', at.column_name_source)
            bk_concatenate += bk_final + "||'" + self.module_dv_char_separator_naming + "'||"
        bk_concatenate = bk_concatenate[:-6-len(self.module_dv_char_separator_naming)]
        hasdiff = md5_function.replace('[x]', bk_concatenate)
        new_dataset_mapping = [all_attributes[0].cod_entity_source, hasdiff,
                               prefix_et + sat_entity_tmp, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        order_by = ''
        if has_ad:
            order_by = ' order by ' + applied_date.column_name_source + ' desc'
        if has_dck:
            hash_md5_function += all_dck_concatenate
        new_dataset_mapping = [sat_cod_entity_source,
                               'ROW_NUMBER() over (partition by ' + hash_md5_function + order_by + ')',
                               prefix_et + sat_entity_tmp, 'RN',
                               integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                               integer_for_metadata[2],
                               sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        ########################### Create Entity STG LAST IMAGE 1 ###########################
        ordinal_position = 1
        new_dataset_mapping = [prefix_et + sat_entity, hash_name, prefix_et + sat_entity_actual_image_1,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity, 'HASHDIFF',
                               prefix_et + sat_entity_actual_image_1, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        all_dck_concatenate = ''
        if has_dck:
            for dck in dependent_child_key:
                all_dck_concatenate += ","+dck.column_name_target
                new_dataset_mapping = [prefix_et + sat_entity, dck.column_name_target, prefix_et + sat_entity_actual_image_1,
                                       dck.column_name_target,
                                       dck.column_type_target, ordinal_position, dck.column_length,
                                       dck.column_precision,
                                       1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        new_dataset_mapping = [prefix_et + sat_entity,
                               'ROW_NUMBER() over (partition by ' + hash_name + ' ' + all_dck_concatenate+ ' ORDER BY DATE_CREATED desc)',
                               prefix_et + sat_entity_actual_image_1, 'RN',
                               integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                               integer_for_metadata[2],
                               sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        ########################### Create Entity STG LAST IMAGE 2 ###########################
        ordinal_position = 1
        new_dataset_mapping = [prefix_et + sat_entity_actual_image_1, hash_name,
                               prefix_et + sat_entity_actual_image_2,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_actual_image_1, 'HASHDIFF',
                               prefix_et + sat_entity_actual_image_2, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_dck:
            for dck in dependent_child_key:
                new_dataset_mapping = [prefix_et + sat_entity_actual_image_1, dck.column_name_target, prefix_et + sat_entity_actual_image_2,
                                       dck.column_name_target,
                                       dck.column_type_target, ordinal_position, dck.column_length,
                                       dck.column_precision,
                                       1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        new_filter = [prefix_et + sat_entity_actual_image_2, 'RN = 1', sat_num_branch, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        ########################### Create Entity STG JOIN ###########################
        ordinal_position = 1

        new_dataset_mapping = [prefix_et + sat_entity_tmp, hash_name,
                               prefix_et + sat_entity_join, hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_tmp, 'HASHDIFF',
                               prefix_et + sat_entity_join, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_rs:
            new_dataset_mapping = [prefix_et + sat_entity_tmp, record_source.column_name_target,
                                   prefix_et + sat_entity_join,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   sat_num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [prefix_et + sat_entity_tmp, applied_date.column_name_target,
                                   prefix_et + sat_entity_join,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   sat_num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_tmp, 'DATE_CREATED',
                               prefix_et + sat_entity_join, 'DATE_CREATED',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + sat_entity_tmp, tn.column_name_target, prefix_et + sat_entity_join,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        if has_dck:
            for dck in dependent_child_key:
                new_dataset_mapping = [prefix_et + sat_entity_tmp, dck.column_name_target, prefix_et + sat_entity_join,
                                       dck.column_name_target,
                                       dck.column_type_target, ordinal_position, dck.column_length,
                                       dck.column_precision,
                                       1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        for at in all_attributes:
            new_dataset_mapping = [prefix_et + sat_entity_tmp, at.column_name_target,
                                   prefix_et + sat_entity_join,
                                   at.column_name_target,
                                   at.column_type_target, ordinal_position, at.column_length,
                                   at.column_precision,
                                   sat_num_branch, at.key_type, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        new_dataset_mapping = [prefix_et + sat_entity_actual_image_2, hash_name,
                               prefix_et + sat_entity_join, hash_name + "_HIST",
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_relationship = [prefix_et + sat_entity_tmp, 'HASHDIFF',
                            prefix_et + sat_entity_actual_image_2,
                            'HASHDIFF', "MASTER JOIN", self.owner]
        self.metadata_actual.add_entry_dataset_relationship([new_relationship])
        new_relationship = [prefix_et + sat_entity_tmp, hash_name,
                            prefix_et + sat_entity_actual_image_2,
                            hash_name, "MASTER JOIN", self.owner]
        self.metadata_actual.add_entry_dataset_relationship([new_relationship])
        if has_dck:
            for dck in dependent_child_key:
                new_relationship = [prefix_et + sat_entity_tmp, dck.column_name_target,
                                    prefix_et + sat_entity_actual_image_2,
                                    dck.column_name_target, "MASTER JOIN", self.owner]
                self.metadata_actual.add_entry_dataset_relationship([new_relationship])

        new_filter = [prefix_et + sat_entity_join, 'RN = 1', sat_num_branch , self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        ########################### Create Entity SAT ###########################
        ordinal_position = 1

        new_dataset_mapping = [prefix_et + sat_entity_join, hash_name,
                               prefix_et + sat_entity, hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_join, 'HASHDIFF',
                               prefix_et + sat_entity, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_rs:
            new_dataset_mapping = [prefix_et + sat_entity_join, record_source.column_name_target,
                                   prefix_et + sat_entity,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   sat_num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [prefix_et + sat_entity_join, applied_date.column_name_target,
                                   prefix_et + sat_entity,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   sat_num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_join, 'DATE_CREATED',
                               prefix_et + sat_entity, 'DATE_CREATED',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + sat_entity_join, tn.column_name_target,
                                       prefix_et + sat_entity,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        if has_dck:
            for dck in dependent_child_key:
                new_dataset_mapping = [prefix_et + sat_entity_join, dck.column_name_target, prefix_et + sat_entity,
                                       dck.column_name_target,
                                       dck.column_type_target, ordinal_position, dck.column_length,
                                       dck.column_precision,
                                       1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        for at in all_attributes:
            new_dataset_mapping = [prefix_et + sat_entity_join, at.column_name_target,
                                   prefix_et + sat_entity,
                                   at.column_name_target,
                                   at.column_type_target, ordinal_position, at.column_length,
                                   at.column_precision,
                                   sat_num_branch, at.key_type, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        new_filter = [prefix_et + sat_entity, hash_name + "_HIST is null", sat_num_branch, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        self.log.log(self.engine_name, "Finished to process Metadata [ Hub satellites - non cdc ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_hub_creation_sat_cdc(self, hub, sat):
        self.log.log(self.engine_name, "Starting to process Metadata [ Hub satellites - cdc ] information", LOG_LEVEL_ONLY_LOG)
        ordinal_position = 1
        prefix_et = 'ET_'
        sat_cod_entity_source = sat[0]
        sat_cod_entity_target = sat[1]
        sat_name = sat[2]
        sat_num_branch = 1 # Sat can't have more than one branch -> sat[3]
        sat_entity = sat_name

        hash_name = 'HASH_' + hub.entity_name
        dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(hub.cod_entity, 0)
        if dv_property is not None: hash_name = dv_property.hash_name

        new_entity_sat_entity_tmp = [prefix_et + sat_entity, sat_entity, ENTITY_TB, hub.cod_path, 'INSERT', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_tmp])

        has_rs = False
        has_tn = False
        has_ad = False
        tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat_num_branch)
        if len(tenant_source) != 0: has_tn = True
        record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat_num_branch)
        if record_source is not None: has_rs = True
        applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(hub.cod_entity, sat[3])
        if applied_date is not None: has_ad = True

        hash_for_metadata = self.connection.get_hash_for_metadata()
        md5_function = self.get_hash_key_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat[3])

        new_dataset_mapping = [sat_cod_entity_source, md5_function, prefix_et + sat_entity,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + sat_entity,
                               'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [sat_cod_entity_source, record_source.column_name_source,
                                   prefix_et + sat_entity,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   sat_num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [sat_cod_entity_source, applied_date.column_name_source,
                                   prefix_et + sat_entity,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   sat_num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [sat_cod_entity_source, tn.column_name_source, prefix_et + sat_entity,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        all_attributes = self.metadata_actual.get_attributes_on_dv_from_satellite_name(sat_entity)

        for at in all_attributes:
            new_dataset_mapping = [at.cod_entity_source, at.column_name_source,
                                   prefix_et + sat_entity,
                                   at.column_name_target,
                                   at.column_type_target, ordinal_position, at.column_length,
                                   at.column_precision,
                                   sat_num_branch, at.key_type, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        md5_function = self.connection.get_md5_function()
        cast_to_string = self.connection.get_cast_string_for_metadata()

        bk_concatenate = ''
        for at in all_attributes:
            bk_final = cast_to_string.replace('[x]', at.column_name_source)
            bk_concatenate += bk_final + "||'" + self.module_dv_char_separator_naming + "'||"
        bk_concatenate = bk_concatenate[:-2]
        hasdiff = md5_function.replace('[x]', bk_concatenate)
        new_dataset_mapping = [all_attributes[0].cod_entity_source, hasdiff,
                               prefix_et + sat_entity, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        self.log.log(self.engine_name, "Finished to process Metadata [ Hub satellites - cdc ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_hub(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Hub ] information", LOG_LEVEL_ONLY_LOG)
        for hub in [x for x in self.metadata_actual.entry_dv_entity if x.entity_type==ENTITY_HUB]:
            self.process_dv_hub_creation_hub(hub)
            self.process_dv_hub_creation_sat(hub)
            self.process_dv_sts(hub)
            self.process_dv_rts(hub)
        self.log.log(self.engine_name, "Finished to process Metadata [ Hub ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_link(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Link ] information", LOG_LEVEL_ONLY_LOG)

        for link in [x for x in self.metadata_actual.entry_dv_entity if x.entity_type == ENTITY_LINK]:
            self.process_dv_link_creation_link(link)
            self.process_dv_link_creation_sat(link)
            self.process_dv_sts(link)
            self.process_dv_rts(link)
            self.process_dv_sate(link)

        self.log.log(self.engine_name, "Finished to process Metadata [ Link ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_sate(self, dv_entity):
        self.log.log(self.engine_name, "Starting to process Metadata [ Effectivity Satellite ] information", LOG_LEVEL_ONLY_LOG)
        ordinal_position = 1
        prefix_et = 'ET_'
        sate_name = dv_entity.name_effectivity_satellite
        sate_entity_actual_image_1 = 'STG_TMP_LAST_IMAGE_1_' + sate_name
        sate_entity_actual_image_2 = 'STG_TMP_LAST_IMAGE_2_' + sate_name
        sate_entity_actual_image_3 = 'STG_TMP_LAST_IMAGE_3_' + sate_name
        sate_entity_union_sources = 'STG_TMP_UNION_' + sate_name
        sate_entity_join = 'STG_TMP_JOIN_' + sate_name
        sate_entity_last_image = 'STG_TMP_LAST_IMAGE_' + sate_name
        sate_entity = sate_name
        cod_entity_target = dv_entity.cod_entity

        hash_name = 'HASH_' + dv_entity.entity_name
        dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(dv_entity.cod_entity, 0)
        if dv_property is not None: hash_name = dv_property.hash_name

        origin_types = self.metadata_actual.get_dict_origin_type_from_cod_entity_on_dv(dv_entity.cod_entity)

        if sate_name is None or sate_name == '': return

        if origin_types['origin_is_total'] == 1 and origin_types['origin_is_incremental'] == 0 and origin_types['origin_is_cdc'] == 0:
            new_entity = [prefix_et + sate_entity_actual_image_1, sate_entity_actual_image_1, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])
            new_entity = [prefix_et + sate_entity_actual_image_2, sate_entity_actual_image_2, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])
            new_entity = [prefix_et + sate_entity_union_sources, sate_entity_union_sources, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])
            new_entity = [prefix_et + sate_entity_join, sate_entity_join, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])
            new_entity = [prefix_et + sate_entity_last_image, sate_entity_last_image, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])
            new_entity = [prefix_et + sate_entity, sate_entity, ENTITY_TB, dv_entity.cod_path, 'INSERT', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])

            has_rs = False
            has_tn = False
            has_ad = False

            ##################################### Union all sources #####################################
            all_sources = self.metadata_actual.get_all_cod_entity_source_from_cod_entity_target_on_entry_dv(cod_entity_target)
            tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
            if len(tenant_source) != 0: has_tn = True
            record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
            if record_source is not None: has_rs = True
            applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, 1)
            if applied_date is not None: has_ad = True

            hash_for_metadata = self.connection.get_hash_for_metadata()

            num_branches = self.metadata_actual.get_num_branches_on_entry_dv_from_cod_entity_name(dv_entity.cod_entity)

            for num_branch in range(1, num_branches + 1):
                entry_dv_mapping_bk = self.metadata_actual.get_all_bk_from_entry_dv_cod_entity_target_and_num_branch(dv_entity.cod_entity, num_branch)
                entry_dv_mapping_bk.sort(key=lambda x: x.ordinal_position)
                cod_entity_source = entry_dv_mapping_bk[0].cod_entity_source
                md5_function = self.get_hash_key_from_cod_entity_target_and_num_branch(cod_entity_target, num_branch)
                new_dataset_mapping = [cod_entity_source, md5_function, prefix_et + sate_entity_union_sources,
                                       hash_name,
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
                new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + sate_entity_union_sources,
                                       'DATE_CREATED',
                                       sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                       sysdate_for_metadata[2], num_branch, None, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

                if has_rs:
                    record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch( cod_entity_target, num_branch)
                    if record_source is not None: has_rs = True
                    new_dataset_mapping = [cod_entity_source, record_source.column_name_source,
                                           prefix_et + sate_entity_union_sources,
                                           record_source.column_name_target,
                                           record_source.column_type_target, ordinal_position,
                                           record_source.column_length,
                                           record_source.column_precision,
                                           num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                if has_tn:
                    if len(tenant_source) != 0: has_tn = True
                    tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, num_branch)
                    for tn in tenant_source:
                        new_dataset_mapping = [cod_entity_source, tn.column_name_source,
                                               prefix_et + sate_entity_union_sources,
                                               tn.column_name_target,
                                               tn.column_type_target, ordinal_position, tn.column_length,
                                               tn.column_precision,
                                               num_branch, KEY_TYPE_TENANT, 1, self.owner]
                        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                        ordinal_position += 1

                if has_ad:
                    applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, num_branch)
                    new_dataset_mapping = [cod_entity_source, applied_date.column_name_source,
                                           prefix_et + sate_entity_union_sources,
                                           applied_date.column_name_target,
                                           applied_date.column_type_target, ordinal_position,
                                           applied_date.column_length,
                                           applied_date.column_precision,
                                           num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            ##################################### LAST IMAGE #####################################
            integer_for_metadata = self.connection.get_integer_for_metadata()
            # Last Image 1
            ordinal_position = 1
            new_dataset_mapping = [prefix_et + sate_entity, hash_name, prefix_et + sate_entity_actual_image_1,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity, 'DATE_START', prefix_et + sate_entity_actual_image_1,
                                   'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity, 'DATE_END', prefix_et + sate_entity_actual_image_1,
                                   'DATE_END',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity, record_source.column_name_target,
                                       prefix_et + sate_entity_actual_image_1,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_dataset_mapping = [prefix_et + sate_entity,
                                   'ROW_NUMBER() over (partition by ' + hash_name + ' ORDER BY DATE_CREATED desc)',
                                   prefix_et + sate_entity_actual_image_1, 'RN',
                                   integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                                   integer_for_metadata[2],
                                   1, KEY_TYPE_NULL, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            # Last Image 2
            ordinal_position = 1
            new_dataset_mapping = [prefix_et + sate_entity_actual_image_1, hash_name,
                                   prefix_et + sate_entity_actual_image_2,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_actual_image_1, 'DATE_START', prefix_et + sate_entity_actual_image_2,
                                   'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_actual_image_1, record_source.column_name_target,
                                       prefix_et + sate_entity_actual_image_2,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_filter = [prefix_et + sate_entity_actual_image_2, 'RN = 1 and DATE_END =' + self.connection.get_sysdate_value_infinite(), 1, self.owner]
            self.metadata_actual.add_entry_filters([new_filter])

            ##################################### JOIN #####################################

            ordinal_position = 1

            new_dataset_mapping = [prefix_et + sate_entity_union_sources, hash_name,
                                   prefix_et + sate_entity_join, hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_union_sources, 'DATE_CREATED',
                                   prefix_et + sate_entity_join, 'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            new_dataset_mapping = ['', self.connection.get_sysdate_value(),
                                   prefix_et + sate_entity_join, 'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            new_dataset_mapping = ['', self.connection.get_sysdate_value_infinite(),
                                   prefix_et + sate_entity_join, 'DATE_END',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1


            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_union_sources, record_source.column_name_target,
                                       prefix_et + sate_entity_join,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])


                new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, record_source.column_name_target,
                                       prefix_et + sate_entity_join,
                                       record_source.column_name_target + "_HIST",
                                       record_source.column_type_target, ordinal_position,
                                       record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity_union_sources, tn.column_name_target,
                                           prefix_et + sate_entity_join,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           1, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                new_dataset_mapping = [prefix_et + sate_entity_union_sources, applied_date.column_name_target,
                                       prefix_et + sate_entity_join,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                       applied_date.column_precision,
                                       1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, hash_name, prefix_et + sate_entity_join,
                                   hash_name + '_HIST',
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, 'DATE_START', prefix_et + sate_entity_join,
                                   'DATE_START_HIST',
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            ####################### Case for Databases that doesn't have OUTER JOIN #######################
            if self.connection.get_connection_type() in CONNECTIONS_WITHOUT_OUTER_JOIN:

                new_relationship = [prefix_et + sate_entity_union_sources, hash_name,
                                    prefix_et + sate_entity_actual_image_2,
                                    hash_name, "MASTER JOIN", self.owner]
                self.metadata_actual.add_entry_dataset_relationship([new_relationship])

                ##### Get another UNION STS to set new relationship
                sate_entity_union_sources_2 = 'STG_TMP_UNION_2_' + sate_name
                new_entity_sts_entity_union_sources = [prefix_et + sate_entity_union_sources_2,
                                                       sate_entity_union_sources_2,
                                                       ENTITY_WITH, dv_entity.cod_path, '', self.owner]
                self.metadata_actual.add_entry_entity([new_entity_sts_entity_union_sources])

                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(
                    cod_entity_target, 1)
                if len(tenant_source) != 0: has_tn = True
                record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(
                    cod_entity_target, 1)
                if record_source is not None: has_rs = True

                hash_for_metadata = self.connection.get_hash_for_metadata()

                new_dataset_mapping = [prefix_et + sate_entity_union_sources, hash_name,
                                       prefix_et + sate_entity_union_sources_2,
                                       hash_name + "_2",
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       1, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
                new_dataset_mapping = [prefix_et + sate_entity_union_sources, 'DATE_CREATED',
                                       prefix_et + sate_entity_union_sources_2,
                                       'DATE_CREATED',
                                       sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                       sysdate_for_metadata[2], 1, None, 1, self.owner]

                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

                if has_rs:
                    new_dataset_mapping = [prefix_et + sate_entity_union_sources, record_source.column_name_target,
                                           prefix_et + sate_entity_union_sources_2,
                                           record_source.column_name_target,
                                           record_source.column_type_target, ordinal_position,
                                           record_source.column_length,
                                           record_source.column_precision,
                                           1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                if has_tn:
                    for tn in tenant_source:
                        new_dataset_mapping = [prefix_et + sate_entity_union_sources, tn.column_name_target,
                                               prefix_et + sate_entity_union_sources_2,
                                               tn.column_name_target,
                                               tn.column_type_target, ordinal_position, tn.column_length,
                                               tn.column_precision,
                                               1, KEY_TYPE_TENANT, 1, self.owner]
                        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                        ordinal_position += 1

                if has_ad:
                    new_dataset_mapping = [prefix_et + sate_entity_union_sources, applied_date.column_name_target,
                                           prefix_et + sate_entity_union_sources_2,
                                           applied_date.column_name_target,
                                           applied_date.column_type_target, ordinal_position,
                                           applied_date.column_length,
                                           applied_date.column_precision,
                                           1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                new_relationship = [prefix_et + sate_entity_actual_image_2, hash_name,
                                    prefix_et + sate_entity_union_sources_2,
                                    hash_name + "_2", "MASTER JOIN", self.owner]
                self.metadata_actual.add_entry_dataset_relationship([new_relationship])

                ##### Set outer join simulation
                ordinal_position = 1

                new_dataset_mapping = [prefix_et + sate_entity_union_sources_2, hash_name + "_2",
                                       prefix_et + sate_entity_join, hash_name,
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       2, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                sysdate_for_metadata = self.connection.get_sysdate_for_metadata()

                new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + sate_entity_join,
                                       'DATE_CREATED',
                                       sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                       sysdate_for_metadata[2], 2, None, 1, self.owner]

                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

                new_dataset_mapping = ['', self.connection.get_sysdate_value(),
                                       prefix_et + sate_entity_join, 'DATE_START',
                                       sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                       sysdate_for_metadata[2], 2, None, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

                new_dataset_mapping = ['', self.connection.get_sysdate_value_infinite(),
                                       prefix_et + sate_entity_join, 'DATE_END',
                                       sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                       sysdate_for_metadata[2], 2, None, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

                if has_rs:
                    new_dataset_mapping = [prefix_et + sate_entity_union_sources_2, record_source.column_name_target,
                                           prefix_et + sate_entity_join,
                                           record_source.column_name_target,
                                           record_source.column_type_target, ordinal_position,
                                           record_source.column_length,
                                           record_source.column_precision,
                                           2, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                    new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, record_source.column_name_target,
                                           prefix_et + sate_entity_join,
                                           record_source.column_name_target + "_HIST",
                                           record_source.column_type_target, ordinal_position,
                                           record_source.column_length,
                                           record_source.column_precision,
                                           2, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                if has_tn:
                    for tn in tenant_source:
                        new_dataset_mapping = [prefix_et + sate_entity_union_sources_2, tn.column_name_target,
                                               prefix_et + sate_entity_join,
                                               tn.column_name_target,
                                               tn.column_type_target, ordinal_position, tn.column_length,
                                               tn.column_precision,
                                               2, KEY_TYPE_TENANT, 1, self.owner]
                        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                        ordinal_position += 1

                if has_ad:
                    new_dataset_mapping = [prefix_et + sate_entity_union_sources_2, applied_date.column_name_target,
                                           prefix_et + sate_entity_join,
                                           applied_date.column_name_target,
                                           applied_date.column_type_target, ordinal_position,
                                           applied_date.column_length,
                                           applied_date.column_precision,
                                           2, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, hash_name, prefix_et + sate_entity_join,
                                       hash_name + '_HIST',
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       2, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, 'DATE_START', prefix_et + sate_entity_join,
                                       'DATE_START_HIST',
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       2, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])


                # Set Filter to the second union
                filter = hash_name + '_2 is null'
                new_filter = [prefix_et + sate_entity_join, filter, 2, self.owner]
                self.metadata_actual.add_entry_filters([new_filter])

            else:
                new_relationship = [prefix_et + sate_entity_union_sources, hash_name,
                                    prefix_et + sate_entity_actual_image_2,
                                    hash_name, "OUTER JOIN", self.owner]
                self.metadata_actual.add_entry_dataset_relationship([new_relationship])


            ##################################### SATE LAST IMAGE #########################################
            new_dataset_mapping = [prefix_et + sate_entity_join, hash_name,
                                   prefix_et + sate_entity_last_image, hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_join, 'DATE_CREATED',
                                   prefix_et + sate_entity_last_image, 'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            new_dataset_mapping = [prefix_et + sate_entity_join, 'DATE_START',
                                   prefix_et + sate_entity_last_image, 'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            new_dataset_mapping = [prefix_et + sate_entity_join, 'DATE_END',
                                   prefix_et + sate_entity_last_image, 'DATE_END',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_join, record_source.column_name_target,
                                       prefix_et + sate_entity_last_image,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position,
                                       record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                new_dataset_mapping = [prefix_et + sate_entity_join, record_source.column_name_target + "_HIST",
                                       prefix_et + sate_entity_last_image,
                                       record_source.column_name_target + "_HIST",
                                       record_source.column_type_target, ordinal_position,
                                       record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity_join, tn.column_name_target,
                                           prefix_et + sate_entity_last_image,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           1, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                new_dataset_mapping = [prefix_et + sate_entity_join, applied_date.column_name_target,
                                       prefix_et + sate_entity_last_image,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position,
                                       applied_date.column_length,
                                       applied_date.column_precision,
                                       1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            integer_for_metadata = self.connection.get_integer_for_metadata()
            date_for_last_image = 'DATE_CREATED'
            if has_ad: date_for_last_image = applied_date.column_name_target
            new_dataset_mapping = [prefix_et + sate_entity_join,
                                   'ROW_NUMBER() over (partition by ' + hash_name + ','+ hash_name + '_HIST ORDER BY ' + date_for_last_image + ' desc)',
                                   prefix_et + sate_entity_last_image, 'RN',
                                   integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                                   integer_for_metadata[2],
                                   1, KEY_TYPE_NULL, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            new_dataset_mapping = [prefix_et + sate_entity_join, hash_name + '_HIST', prefix_et + sate_entity_last_image,
                                   hash_name + '_HIST',
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_dataset_mapping = [prefix_et + sate_entity_join, 'DATE_START_HIST',
                                   prefix_et + sate_entity_last_image,
                                   'DATE_START_HIST',
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            ###################################### SATE  ######################################
            # Branch 1: Insert if only exists on source
            new_dataset_mapping = [prefix_et + sate_entity_last_image, hash_name,
                                   prefix_et + sate_entity, hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_last_image, 'DATE_CREATED',
                                   prefix_et + sate_entity, 'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            new_dataset_mapping = [prefix_et + sate_entity_last_image, 'DATE_START',
                                   prefix_et + sate_entity, 'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            new_dataset_mapping = [prefix_et + sate_entity_last_image, 'DATE_END',
                                   prefix_et + sate_entity, 'DATE_END',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_last_image, record_source.column_name_target,
                                       prefix_et + sate_entity,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position,
                                       record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity_last_image, tn.column_name_target,
                                           prefix_et + sate_entity,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           1, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                new_dataset_mapping = [prefix_et + sate_entity_last_image, applied_date.column_name_target,
                                       prefix_et + sate_entity,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position,
                                       applied_date.column_length,
                                       applied_date.column_precision,
                                       1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            filter = hash_name + "_HIST is null and RN = 1"
            new_filter = [prefix_et + sate_entity, filter, 1, self.owner]
            self.metadata_actual.add_entry_filters([new_filter])

            # Branch 2: Insert if only exists on target
            new_dataset_mapping = [prefix_et + sate_entity_last_image, hash_name+"_HIST",
                                   prefix_et + sate_entity, hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   2, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_last_image, 'DATE_CREATED',
                                   prefix_et + sate_entity, 'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 2, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            new_dataset_mapping = [prefix_et + sate_entity_last_image, 'DATE_START_HIST',
                                   prefix_et + sate_entity, 'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 2, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            new_dataset_mapping = [prefix_et + sate_entity_last_image, 'DATE_START',
                                   prefix_et + sate_entity, 'DATE_END',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 2, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_last_image, record_source.column_name_target + "_HIST",
                                       prefix_et + sate_entity,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position,
                                       record_source.column_length,
                                       record_source.column_precision,
                                       2, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity_last_image, tn.column_name_target,
                                           prefix_et + sate_entity,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           2, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                new_dataset_mapping = [prefix_et + sate_entity_last_image, applied_date.column_name_target,
                                       prefix_et + sate_entity,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position,
                                       applied_date.column_length,
                                       applied_date.column_precision,
                                       2, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            filter = hash_name + " is null and RN = 1"
            new_filter = [prefix_et + sate_entity, filter, 2, self.owner]
            self.metadata_actual.add_entry_filters([new_filter])

        elif origin_types['origin_is_incremental'] == 1 or origin_types['origin_is_cdc'] == 1:
            new_entity = [prefix_et + sate_entity_actual_image_1, sate_entity_actual_image_1, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])
            new_entity = [prefix_et + sate_entity_actual_image_2, sate_entity_actual_image_2, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])
            new_entity = [prefix_et + sate_entity_actual_image_3, sate_entity_actual_image_3, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])
            new_entity = [prefix_et + sate_entity_union_sources, sate_entity_union_sources, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])
            new_entity = [prefix_et + sate_entity_join, sate_entity_join, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])
            new_entity = [prefix_et + sate_entity, sate_entity, ENTITY_TB, dv_entity.cod_path, 'INSERT', self.owner]
            self.metadata_actual.add_entry_entity([new_entity])

            has_rs = False
            has_tn = False
            has_ad = False

            ##################################### Union all sources #####################################
            tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
            if len(tenant_source) != 0: has_tn = True
            record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
            if record_source is not None: has_rs = True
            applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, 1)
            if applied_date is not None: has_ad = True

            hash_for_metadata = self.connection.get_hash_for_metadata()

            num_branches = self.metadata_actual.get_num_branches_on_entry_dv_from_cod_entity_name(dv_entity.cod_entity)

            for num_branch in range(1, num_branches + 1):
                entry_dv_mapping_bk = self.metadata_actual.get_all_bk_from_entry_dv_cod_entity_target_and_num_branch(dv_entity.cod_entity, num_branch)
                entry_dv_mapping_bk.sort(key=lambda x: x.ordinal_position)
                cod_entity_source = entry_dv_mapping_bk[0].cod_entity_source
                md5_function = self.get_hash_key_from_cod_entity_target_and_num_branch(cod_entity_target, num_branch)
                new_dataset_mapping = [cod_entity_source, md5_function, prefix_et + sate_entity_union_sources,
                                       hash_name,
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
                new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + sate_entity_union_sources,
                                       'DATE_CREATED',
                                       sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                       sysdate_for_metadata[2], num_branch, None, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

                if has_rs:
                    record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(
                        cod_entity_target, num_branch)
                    if record_source is not None: has_rs = True
                    new_dataset_mapping = [cod_entity_source, record_source.column_name_source,
                                           prefix_et + sate_entity_union_sources,
                                           record_source.column_name_target,
                                           record_source.column_type_target, ordinal_position,
                                           record_source.column_length,
                                           record_source.column_precision,
                                           num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                if has_tn:
                    if len(tenant_source) != 0: has_tn = True
                    tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, num_branch)
                    for tn in tenant_source:
                        new_dataset_mapping = [cod_entity_source, tn.column_name_source,
                                               prefix_et + sate_entity_union_sources,
                                               tn.column_name_target,
                                               tn.column_type_target, ordinal_position, tn.column_length,
                                               tn.column_precision,
                                               num_branch, KEY_TYPE_TENANT, 1, self.owner]
                        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                        ordinal_position += 1

                if has_ad:
                    applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(
                        dv_entity.cod_entity, num_branch)
                    new_dataset_mapping = [cod_entity_source, applied_date.column_name_source,
                                           prefix_et + sate_entity_union_sources,
                                           applied_date.column_name_target,
                                           applied_date.column_type_target, ordinal_position,
                                           applied_date.column_length,
                                           applied_date.column_precision,
                                           num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

                # Get Driven Key num_connection
                all_connections_with_dk = self.metadata_actual.get_list_num_connection_with_driven_key_from_cod_entity_target(dv_entity.cod_entity)
                all_hashes_from_dk = []
                for num_con in all_connections_with_dk:
                    hash_name_hub = 'HASH_' + str(num_con)
                    dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(dv_entity.cod_entity, num_con)
                    if dv_property is not None: hash_name_hub = dv_property.hash_name
                    all_hashes_from_dk.append(hash_name_hub)
                    hash_key = self.get_hash_key_from_cod_entity_target_and_num_branch_and_num_connection(cod_entity_target, num_branch, num_con)
                    new_dataset_mapping = [cod_entity_source, hash_key,
                                           prefix_et + sate_entity_union_sources,
                                           hash_name_hub,
                                           hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                           hash_for_metadata[2],
                                           num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            ##################################### LAST IMAGE #####################################
            integer_for_metadata = self.connection.get_integer_for_metadata()
            # Last Image 1
            ordinal_position = 1
            new_dataset_mapping = [prefix_et + sate_entity, hash_name, prefix_et + sate_entity_actual_image_1,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity, 'DATE_START', prefix_et + sate_entity_actual_image_1,
                                   'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity, 'DATE_END', prefix_et + sate_entity_actual_image_1,
                                   'DATE_END',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity, record_source.column_name_target,
                                       prefix_et + sate_entity_actual_image_1,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity, tn.column_name_target,
                                           prefix_et + sate_entity_union_sources,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           1, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(cod_entity_target, 1)
                new_dataset_mapping = [prefix_et + sate_entity, applied_date.column_name_target,
                                       prefix_et + sate_entity_union_sources,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position,
                                       applied_date.column_length,
                                       applied_date.column_precision,
                                       1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_dataset_mapping = [prefix_et + sate_entity,
                                   'ROW_NUMBER() over (partition by ' + hash_name + ' ORDER BY DATE_CREATED desc)',
                                   prefix_et + sate_entity_actual_image_1, 'RN',
                                   integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                                   integer_for_metadata[2],
                                   1, KEY_TYPE_NULL, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            # Last Image 2
            ordinal_position = 1
            new_dataset_mapping = [prefix_et + sate_entity_actual_image_1, hash_name,
                                   prefix_et + sate_entity_actual_image_2,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_actual_image_1, 'DATE_START',
                                   prefix_et + sate_entity_actual_image_2,
                                   'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_actual_image_1, record_source.column_name_target,
                                       prefix_et + sate_entity_actual_image_2,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity_actual_image_1, tn.column_name_target,
                                           prefix_et + sate_entity_actual_image_2,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           1, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(cod_entity_target, 1)
                new_dataset_mapping = [prefix_et + sate_entity_actual_image_1, applied_date.column_name_target,
                                       prefix_et + sate_entity_actual_image_2,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position,
                                       applied_date.column_length,
                                       applied_date.column_precision,
                                       1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_filter = [prefix_et + sate_entity_actual_image_2,
                          'RN = 1 and DATE_END =' + self.connection.get_sysdate_value_infinite(), 1, self.owner]
            self.metadata_actual.add_entry_filters([new_filter])

            ##################################### LAST IMAGE - Including Driven Key #####################################

            # Relationship to get Driven Key Hash
            new_relationship = [prefix_et + sate_entity_actual_image_2, hash_name,
                                cod_entity_target,
                                hash_name, "MASTER JOIN", self.owner]
            self.metadata_actual.add_entry_dataset_relationship([new_relationship])

            ordinal_position = 1
            new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, hash_name,
                                   prefix_et + sate_entity_actual_image_3,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, 'DATE_START',
                                   prefix_et + sate_entity_actual_image_3,
                                   'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, record_source.column_name_target,
                                       prefix_et + sate_entity_actual_image_3,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, tn.column_name_target,
                                           prefix_et + sate_entity_actual_image_3,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           1, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(cod_entity_target, 1)
                new_dataset_mapping = [prefix_et + sate_entity_actual_image_2, applied_date.column_name_target,
                                       prefix_et + sate_entity_actual_image_3,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position,
                                       applied_date.column_length,
                                       applied_date.column_precision,
                                       1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            #Get Driven Key num_connection
            all_connections_with_dk = self.metadata_actual.get_list_num_connection_with_driven_key_from_cod_entity_target(dv_entity.cod_entity)
            all_hashes_from_dk = []
            for num_con in all_connections_with_dk:
                hash_name_hub = 'HASH_' + str(num_con)
                dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(dv_entity.cod_entity, num_con)
                if dv_property is not None: hash_name_hub = dv_property.hash_name
                all_hashes_from_dk.append(hash_name_hub)
                new_dataset_mapping = [cod_entity_target, hash_name_hub,
                                       prefix_et + sate_entity_actual_image_3,
                                       hash_name_hub,
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       1, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            ################################## JOIN #############################################

            ordinal_position = 1
            new_dataset_mapping = [prefix_et + sate_entity_actual_image_3, hash_name,
                                   prefix_et + sate_entity_join,
                                   hash_name +"_HIST",
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_actual_image_3, 'DATE_START',
                                   prefix_et + sate_entity_join,
                                   'DATE_START_HIST',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_actual_image_3, record_source.column_name_target,
                                       prefix_et + sate_entity_join,
                                       record_source.column_name_target+"_HIST",
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity_actual_image_3, tn.column_name_target,
                                           prefix_et + sate_entity_join,
                                           tn.column_name_target+"_HIST",
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           1, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(cod_entity_target, 1)
                new_dataset_mapping = [prefix_et + sate_entity_actual_image_3, applied_date.column_name_target,
                                       prefix_et + sate_entity_join,
                                       applied_date.column_name_target+"_HIST",
                                       applied_date.column_type_target, ordinal_position,
                                       applied_date.column_length,
                                       applied_date.column_precision,
                                       1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            for hash_dk in all_hashes_from_dk:
                new_dataset_mapping = [prefix_et + sate_entity_actual_image_3, hash_dk,
                                       prefix_et + sate_entity_join,
                                       hash_dk+"_HIST",
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       1, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_dataset_mapping = [prefix_et + sate_entity_union_sources, hash_name, prefix_et + sate_entity_join,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_union_sources, 'DATE_CREATED',
                                   prefix_et + sate_entity_join,
                                   'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_union_sources, record_source.column_name_target,
                                       prefix_et + sate_entity_join,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position,
                                       record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                if len(tenant_source) != 0: has_tn = True
                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity_union_sources, tn.column_name_target,
                                           prefix_et + sate_entity_join,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           1, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(cod_entity_target, 1)
                new_dataset_mapping = [prefix_et + sate_entity_union_sources, applied_date.column_name_source,
                                       prefix_et + sate_entity_join,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position,
                                       applied_date.column_length,
                                       applied_date.column_precision,
                                       1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            for hash_dk in all_hashes_from_dk:
                new_dataset_mapping = [prefix_et + sate_entity_union_sources, hash_dk,
                                       prefix_et + sate_entity_join,
                                       hash_dk,
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       1, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])


                new_relationship = [prefix_et + sate_entity_union_sources, hash_dk,
                                    prefix_et + sate_entity_actual_image_3,
                                    hash_dk, "MASTER JOIN", self.owner]
                self.metadata_actual.add_entry_dataset_relationship([new_relationship])

            ##################################### SATE #####################################

            # Branch 1 - exsits only on source
            ordinal_position = 1
            new_dataset_mapping = [prefix_et + sate_entity_join, hash_name,
                                   prefix_et + sate_entity,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_join, 'DATE_CREATED',
                                   prefix_et + sate_entity,
                                   'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_join, self.connection.get_sysdate_value_infinite(),
                                   prefix_et + sate_entity,
                                   'DATE_END',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_join, 'DATE_CREATED',
                                   prefix_et + sate_entity,
                                   'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_join, record_source.column_name_target,
                                       prefix_et + sate_entity,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(
                    cod_entity_target, 1)
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity_join, tn.column_name_target,
                                           prefix_et + sate_entity,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           1, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(cod_entity_target, 1)
                new_dataset_mapping = [prefix_et + sate_entity_join, applied_date.column_name_target,
                                       prefix_et + sate_entity,
                                       applied_date.column_name_target ,
                                       applied_date.column_type_target, ordinal_position,
                                       applied_date.column_length,
                                       applied_date.column_precision,
                                       1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_filter = [prefix_et + sate_entity, hash_name + ' <> ' + hash_name+'_HIST or ' + hash_name + '_HIST is null', 1, self.owner]
            self.metadata_actual.add_entry_filters([new_filter])

            # Branch 2 - relation udpated -> DELETE actual relation
            ordinal_position = 1
            new_dataset_mapping = [prefix_et + sate_entity_join, hash_name +'_HIST',
                                   prefix_et + sate_entity,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   2, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_join, 'DATE_START_HIST',
                                   prefix_et + sate_entity,
                                   'DATE_START',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 2, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_join, 'DATE_CREATED',
                                   prefix_et + sate_entity,
                                   'DATE_END',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 2, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sate_entity_join, 'DATE_CREATED',
                                   prefix_et + sate_entity,
                                   'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 2, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sate_entity_join, record_source.column_name_target,
                                       prefix_et + sate_entity,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       2, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(
                    cod_entity_target, 1)
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sate_entity_join, tn.column_name_target,
                                           prefix_et + sate_entity,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           2, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(cod_entity_target, 1)
                new_dataset_mapping = [prefix_et + sate_entity_join, applied_date.column_name_target,
                                       prefix_et + sate_entity,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position,
                                       applied_date.column_length,
                                       applied_date.column_precision,
                                       2, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_filter = [prefix_et + sate_entity,
                          hash_name + ' <> ' + hash_name + '_HIST', 2, self.owner]
            self.metadata_actual.add_entry_filters([new_filter])

        self.log.log(self.engine_name, "Finished to process Metadata [ Effectivity Satellite ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_sts(self, dv_entity):
        self.log.log(self.engine_name, "Starting to process Metadata [ Status Tracking Satellite ] information", LOG_LEVEL_ONLY_LOG)

        ordinal_position = 1
        prefix_et = 'ET_'
        sts_name = dv_entity.name_status_tracking_satellite
        sts_entity_actual_image_1 = 'STG_TMP_LAST_IMAGE_1_' + sts_name
        sts_entity_actual_image_2 = 'STG_TMP_LAST_IMAGE_2_' + sts_name
        sts_entity_union_sources = 'STG_TMP_UNION_' + sts_name
        sts_entity_join = 'STG_TMP_JOIN_' + sts_name
        sts_entity = sts_name
        cod_entity_target = dv_entity.cod_entity

        hash_name = 'HASH_' + dv_entity.entity_name
        dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(dv_entity.cod_entity, 0)
        if dv_property is not None: hash_name = dv_property.hash_name

        if sts_name is None or sts_name == '': return

        new_entity_sts_entity_actual_image_1 = [prefix_et + sts_entity_actual_image_1, sts_entity_actual_image_1, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sts_entity_actual_image_1])
        new_entity_sts_entity_actual_image_2 = [prefix_et + sts_entity_actual_image_2, sts_entity_actual_image_2, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sts_entity_actual_image_2])
        new_entity_sts_entity_union_sources = [prefix_et + sts_entity_union_sources, sts_entity_union_sources, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sts_entity_union_sources])
        new_entity_sts_entity_join = [prefix_et + sts_entity_join, sts_entity_join, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sts_entity_join])
        new_entity_sts_entity = [prefix_et + sts_entity, sts_entity, ENTITY_TB, dv_entity.cod_path, 'INSERT', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sts_entity])

        has_rs = False
        has_tn = False
        has_ad = False

        ##################################### Union all sources #####################################
        all_sources = self.metadata_actual.get_all_cod_entity_source_from_cod_entity_target_on_entry_dv(cod_entity_target)
        tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
        if len(tenant_source) != 0: has_tn = True
        record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
        if record_source is not None: has_rs = True
        applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, 1)
        if applied_date is not None: has_ad = True


        hash_for_metadata = self.connection.get_hash_for_metadata()

        num_branches = self.metadata_actual.get_num_branches_on_entry_dv_from_cod_entity_name(dv_entity.cod_entity)

        for num_branch in range(1, num_branches + 1):
            entry_dv_mapping_bk = self.metadata_actual.get_all_bk_from_entry_dv_cod_entity_target_and_num_branch(dv_entity.cod_entity, num_branch)
            entry_dv_mapping_bk.sort(key=lambda x: x.ordinal_position)
            cod_entity_source = entry_dv_mapping_bk[0].cod_entity_source
            md5_function = self.get_hash_key_from_cod_entity_target_and_num_branch(cod_entity_target, num_branch)
            new_dataset_mapping = [cod_entity_source, md5_function, prefix_et + sts_entity_union_sources,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + sts_entity_union_sources,
                                   'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], num_branch, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, num_branch)
                new_dataset_mapping = [cod_entity_source, record_source.column_name_source,
                                       prefix_et + sts_entity_union_sources,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, num_branch)
                for tn in tenant_source:
                    new_dataset_mapping = [cod_entity_source, tn.column_name_source, prefix_et + sts_entity_union_sources,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           num_branch, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, num_branch)
                new_dataset_mapping = [cod_entity_source, applied_date.column_name_source,
                                       prefix_et + sts_entity_union_sources,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                       applied_date.column_precision,
                                       num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        ##################################### LAST IMAGE #####################################
        integer_for_metadata = self.connection.get_integer_for_metadata()
        # Last Image 1
        ordinal_position = 1
        new_dataset_mapping = [prefix_et + sts_entity, hash_name, prefix_et + sts_entity_actual_image_1, hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               1, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        varchar_for_metadata = self.connection.get_string_for_metadata()
        new_dataset_mapping = [prefix_et + sts_entity, 'DV_STATUS', prefix_et + sts_entity_actual_image_1, 'DV_STATUS',
                               varchar_for_metadata[0], ordinal_position, 1, 0,
                               1, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sts_entity,
                               'ROW_NUMBER() over (partition by ' + hash_name + ' ORDER BY DATE_CREATED desc)',
                               prefix_et + sts_entity_actual_image_1, 'RN',
                               integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                               integer_for_metadata[2],
                               1, KEY_TYPE_NULL, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_rs:
            record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
            new_dataset_mapping = [prefix_et + sts_entity, record_source.column_name_target,
                                   prefix_et + sts_entity_actual_image_1,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + sts_entity, tn.column_name_target, prefix_et + sts_entity_actual_image_1,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        if has_ad:
            applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, 1)
            new_dataset_mapping = [prefix_et + sts_entity, applied_date.column_name_target,
                                   prefix_et + sts_entity_actual_image_1,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        # Last Image 2
        ordinal_position = 1
        new_dataset_mapping = [prefix_et + sts_entity_actual_image_1, hash_name,
                               prefix_et + sts_entity_actual_image_2,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               1, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        varchar_for_metadata = self.connection.get_string_for_metadata()
        new_dataset_mapping = [prefix_et + sts_entity_actual_image_1, 'DV_STATUS', prefix_et + sts_entity_actual_image_2, 'DV_STATUS',
                               varchar_for_metadata[0], ordinal_position, 1, 0,
                               1, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_rs:
            record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(
                cod_entity_target, 1)
            new_dataset_mapping = [prefix_et + sts_entity_actual_image_1, record_source.column_name_target,
                                   prefix_et + sts_entity_actual_image_2,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(
                cod_entity_target, 1)
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + sts_entity_actual_image_1, tn.column_name_target,
                                       prefix_et + sts_entity_actual_image_2,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        if has_ad:
            applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, 1)
            new_dataset_mapping = [prefix_et + sts_entity_actual_image_1, applied_date.column_name_target,
                                   prefix_et + sts_entity_actual_image_2,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_filter = [prefix_et + sts_entity_actual_image_2, 'RN = 1', 1, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        ##################################### JOIN #####################################

        ordinal_position = 1

        new_dataset_mapping = [prefix_et + sts_entity_union_sources, hash_name,
                               prefix_et + sts_entity_join, hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               1, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = [prefix_et + sts_entity_union_sources, 'DATE_CREATED',
                               prefix_et + sts_entity_join, 'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], 1, None, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        varchar_for_metadata = self.connection.get_string_for_metadata()
        new_dataset_mapping = ['', "'I'",
                               prefix_et + sts_entity_join, 'DV_STATUS_INSERT',
                               varchar_for_metadata[0], ordinal_position, 1,
                               varchar_for_metadata[2], 1, None, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        varchar_for_metadata = self.connection.get_string_for_metadata()
        new_dataset_mapping = ['', "'D'",
                               prefix_et + sts_entity_join, 'DV_STATUS_DELETE',
                               varchar_for_metadata[0], ordinal_position, 1,
                               varchar_for_metadata[2], 1, None, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        varchar_for_metadata = self.connection.get_string_for_metadata()
        new_dataset_mapping = ['', "'U'",
                               prefix_et + sts_entity_join, 'DV_STATUS_UPDATE',
                               varchar_for_metadata[0], ordinal_position, 1,
                               varchar_for_metadata[2], 1, None, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [prefix_et + sts_entity_union_sources, record_source.column_name_target,
                                   prefix_et + sts_entity_join,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + sts_entity_union_sources, tn.column_name_target,
                                       prefix_et + sts_entity_join,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        if has_ad:
            new_dataset_mapping = [prefix_et + sts_entity_union_sources, applied_date.column_name_target,
                                   prefix_et + sts_entity_join,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sts_entity_actual_image_2, hash_name, prefix_et + sts_entity_join, hash_name + '_HIST',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               1, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sts_entity_actual_image_2, 'DV_STATUS',
                               prefix_et + sts_entity_join, 'DV_STATUS_HIST',
                               varchar_for_metadata[0], ordinal_position, 1, 0,
                               1, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_rs:
            record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(
                cod_entity_target, 1)
            new_dataset_mapping = [prefix_et + sts_entity_actual_image_2, record_source.column_name_target,
                                   prefix_et + sts_entity_join,
                                   record_source.column_name_target + "_HIST",
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(
                cod_entity_target, 1)
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + sts_entity_actual_image_2, tn.column_name_target,
                                       prefix_et + sts_entity_join,
                                       tn.column_name_target + "_HIST",
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        if has_ad:
            applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, 1)
            new_dataset_mapping = [prefix_et + sts_entity_actual_image_2, applied_date.column_name_target,
                                   prefix_et + sts_entity_join,
                                   applied_date.column_name_target + "_HIST",
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])



        ####################### Case for Databases that doesn't have OUTER JOIN #######################
        if self.connection.get_connection_type() in CONNECTIONS_WITHOUT_OUTER_JOIN:

            new_relationship = [prefix_et + sts_entity_union_sources, hash_name,
                                prefix_et + sts_entity_actual_image_2,
                                hash_name, "MASTER JOIN", self.owner]
            self.metadata_actual.add_entry_dataset_relationship([new_relationship])

            ##### Get another UNION STS to set new relationship
            sts_entity_union_sources_2 = 'STG_TMP_UNION_2_' + sts_name
            new_entity_sts_entity_union_sources = [prefix_et + sts_entity_union_sources_2, sts_entity_union_sources_2,
                                                   ENTITY_WITH, dv_entity.cod_path, '', self.owner]
            self.metadata_actual.add_entry_entity([new_entity_sts_entity_union_sources])

            tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
            if len(tenant_source) != 0: has_tn = True
            record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
            if record_source is not None: has_rs = True

            hash_for_metadata = self.connection.get_hash_for_metadata()

            new_dataset_mapping = [prefix_et + sts_entity_union_sources, hash_name , prefix_et + sts_entity_union_sources_2,
                                   hash_name+ "_2",
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sts_entity_union_sources, 'DATE_CREATED', prefix_et + sts_entity_union_sources_2,
                                   'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 1, None, 1, self.owner]

            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [prefix_et + sts_entity_union_sources, record_source.column_name_target,
                                       prefix_et + sts_entity_union_sources_2,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position,
                                       record_source.column_length,
                                       record_source.column_precision,
                                       1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sts_entity_union_sources, tn.column_name_target,
                                           prefix_et + sts_entity_union_sources_2,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           1, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                new_dataset_mapping = [prefix_et + sts_entity_union_sources, applied_date.column_name_target,
                                       prefix_et + sts_entity_union_sources_2,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                       applied_date.column_precision,
                                       1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_relationship = [prefix_et + sts_entity_actual_image_2, hash_name,
                                prefix_et + sts_entity_union_sources_2,
                                hash_name+ "_2", "MASTER JOIN", self.owner]
            self.metadata_actual.add_entry_dataset_relationship([new_relationship])


            ##### Set outer join simulation
            ordinal_position = 1

            new_dataset_mapping = [prefix_et + sts_entity_union_sources_2, hash_name + "_2",
                                   prefix_et + sts_entity_join, hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   2, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()

            new_dataset_mapping = [prefix_et + sts_entity_union_sources_2, 'DATE_CREATED', prefix_et + sts_entity_join,
                                   'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], 2, None, 1, self.owner]

            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            varchar_for_metadata = self.connection.get_string_for_metadata()
            new_dataset_mapping = ['', "'I'",
                                   prefix_et + sts_entity_join, 'DV_STATUS_INSERT',
                                   varchar_for_metadata[0], ordinal_position, 1,
                                   varchar_for_metadata[2], 2, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            varchar_for_metadata = self.connection.get_string_for_metadata()
            new_dataset_mapping = ['', "'D'",
                                   prefix_et + sts_entity_join, 'DV_STATUS_DELETE',
                                   varchar_for_metadata[0], ordinal_position, 1,
                                   varchar_for_metadata[2], 2, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            varchar_for_metadata = self.connection.get_string_for_metadata()
            new_dataset_mapping = ['', "'U'",
                                   prefix_et + sts_entity_join, 'DV_STATUS_UPDATE',
                                   varchar_for_metadata[0], ordinal_position, 1,
                                   varchar_for_metadata[2], 2, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
                new_dataset_mapping = [prefix_et + sts_entity_union_sources_2, record_source.column_name_target,
                                       prefix_et + sts_entity_join,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       2, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(cod_entity_target, 1)
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sts_entity_union_sources_2, tn.column_name_target,
                                           prefix_et + sts_entity_join,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           2, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, 1)
                new_dataset_mapping = [prefix_et + sts_entity_union_sources_2, applied_date.column_name_target,
                                       prefix_et + sts_entity_join,
                                       applied_date.column_name_target ,
                                       applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                       applied_date.column_precision,
                                       2, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])


            new_dataset_mapping = [prefix_et + sts_entity_actual_image_2, hash_name, prefix_et + sts_entity_join,
                                   hash_name + '_HIST',
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   2, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            new_dataset_mapping = [prefix_et + sts_entity_actual_image_2, 'DV_STATUS',
                                   prefix_et + sts_entity_join, 'DV_STATUS_HIST',
                                   varchar_for_metadata[0], ordinal_position, 1, 0,
                                   2, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_rs:
                record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(
                    cod_entity_target, 1)
                new_dataset_mapping = [prefix_et + sts_entity_actual_image_2, record_source.column_name_target,
                                       prefix_et + sts_entity_join,
                                       record_source.column_name_target + "_HIST",
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       2, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(
                    cod_entity_target, 1)
                for tn in tenant_source:
                    new_dataset_mapping = [prefix_et + sts_entity_actual_image_2, tn.column_name_target,
                                           prefix_et + sts_entity_join,
                                           tn.column_name_target + "_HIST",
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           2, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity,
                                                                                                  1)
                new_dataset_mapping = [prefix_et + sts_entity_actual_image_2, applied_date.column_name_target,
                                       prefix_et + sts_entity_join,
                                       applied_date.column_name_target + "_HIST",
                                       applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                       applied_date.column_precision,
                                       2, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            # Set Filter to the second union
            filter = hash_name + '_2 is null'
            new_filter = [prefix_et + sts_entity_join, filter, 2, self.owner]
            self.metadata_actual.add_entry_filters([new_filter])

        else:
            new_relationship = [prefix_et + sts_entity_union_sources, hash_name,
                                prefix_et + sts_entity_actual_image_2,
                                hash_name, "OUTER JOIN", self.owner]
            self.metadata_actual.add_entry_dataset_relationship([new_relationship])

        ##################################### STS #####################################

        origin_types = self.metadata_actual.get_dict_origin_type_from_cod_entity_on_dv(dv_entity.cod_entity)
        for num_branch_sts in [1,2,3]:
            # Incremental and CDC origin can't have 'D' options.
            if (origin_types['origin_is_incremental'] == 1 or origin_types['origin_is_cdc'] == 1) and num_branch_sts == 2: continue
            ordinal_position = 1

            if num_branch_sts == 1 or num_branch_sts == 3:
                new_dataset_mapping = [prefix_et + sts_entity_join, hash_name,
                                       prefix_et + sts_entity, hash_name,
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                       num_branch_sts, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if num_branch_sts == 2:
                new_dataset_mapping = [prefix_et + sts_entity_join, hash_name + "_HIST",
                                       prefix_et + sts_entity, hash_name,
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       num_branch_sts, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            date_created = 'DATE_CREATED'
            if num_branch_sts == 2: date_created = self.connection.get_sysdate_value()
            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = [prefix_et + sts_entity_join, date_created,
                                   prefix_et + sts_entity, 'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], num_branch_sts, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                column_name_target = record_source.column_name_target
                if num_branch_sts == 2: column_name_target = record_source.column_name_target +"_HIST"
                new_dataset_mapping = [prefix_et + sts_entity_join, column_name_target,
                                       prefix_et + sts_entity,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       num_branch_sts, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                for tn in tenant_source:
                    column_name_target = tn.column_name_target
                    if num_branch_sts == 2: column_name_target = tn.column_name_target + "_HIST"
                    new_dataset_mapping = [prefix_et + sts_entity_join, column_name_target,
                                           prefix_et + sts_entity,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           num_branch_sts, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            if has_ad:
                column_name_target = applied_date.column_name_target
                if num_branch_sts == 2: column_name_target = applied_date.column_name_target + "_HIST"
                new_dataset_mapping = [prefix_et + sts_entity_join, column_name_target,
                                       prefix_et + sts_entity,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                       applied_date.column_precision,
                                       num_branch_sts, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            # Case INSERT
            if num_branch_sts == 1:
                new_dataset_mapping = [prefix_et + sts_entity_join, 'DV_STATUS_INSERT',
                                       prefix_et + sts_entity, 'DV_STATUS',
                                       varchar_for_metadata[0], ordinal_position, 1,
                                       0, num_branch_sts, None, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

                filter = hash_name + "_HIST is null or ( DV_STATUS_HIST = DV_STATUS_DELETE and "+ hash_name +" is not null)"
                new_filter = [prefix_et + sts_entity, filter, num_branch_sts, self.owner]
                self.metadata_actual.add_entry_filters([new_filter])

            # Case DELETE
            if num_branch_sts == 2:
                new_dataset_mapping = [prefix_et + sts_entity_join, 'DV_STATUS_DELETE',
                                       prefix_et + sts_entity, 'DV_STATUS',
                                       varchar_for_metadata[0], ordinal_position, 1,
                                       0, num_branch_sts, None, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

                filter = hash_name + ' is null and DV_STATUS_DELETE != DV_STATUS_HIST'
                new_filter = [prefix_et + sts_entity, filter, num_branch_sts, self.owner]
                self.metadata_actual.add_entry_filters([new_filter])

            # Case UPDATE
            if num_branch_sts == 3:
                new_dataset_mapping = [prefix_et + sts_entity_join, 'DV_STATUS_UPDATE',
                                       prefix_et + sts_entity, 'DV_STATUS',
                                       varchar_for_metadata[0], ordinal_position, 1,
                                       0, num_branch_sts, None, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

                filter = hash_name + ' is not null and ' + hash_name +"_HIST is not null and DV_STATUS_UPDATE != DV_STATUS_HIST and DV_STATUS_HIST != DV_STATUS_DELETE "
                new_filter = [prefix_et + sts_entity, filter, num_branch_sts, self.owner]
                self.metadata_actual.add_entry_filters([new_filter])

        self.log.log(self.engine_name, "Finished to process Metadata [ Status Tracking Satellite ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_rts(self, dv_entity):
        self.log.log(self.engine_name, "Starting to process Metadata [ Record Tracking Satellite ] information", LOG_LEVEL_ONLY_LOG)

        ordinal_position = 1
        prefix_et = 'ET_'
        sat_cod_entity_target = dv_entity.cod_entity
        sat_name = dv_entity.name_record_tracking_satellite
        sat_num_branch = 1  # Sat can't have more than one branch -> sat[3]

        hash_name = 'HASH_' + dv_entity.entity_name

        if sat_name is None or sat_name == '': return

        dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(dv_entity.cod_entity, 0)
        if dv_property is not None: hash_name = dv_property.hash_name


        ########################### Create all entities ###########################
        sat_entity_tmp = 'STG_TMP_' + sat_name
        sat_entity_tmp_last_applied_date = 'STG_TMP_LAST_APPLIED_DATE_' + sat_name
        sat_entity_actual_image_1 = 'STG_TMP_LAST_IMAGE_1_' + sat_name
        sat_entity_actual_image_2 = 'STG_TMP_LAST_IMAGE_2_' + sat_name
        sat_entity_join = 'STG_TMP_JOIN_' + sat_name
        sat_entity = sat_name

        new_entity_sat_entity_tmp = [prefix_et + sat_entity_tmp, sat_entity_tmp, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_tmp])
        new_entity_sat_entity_tmp = [prefix_et + sat_entity_tmp_last_applied_date, sat_entity_tmp_last_applied_date, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_tmp])
        new_entity_sat_entity_actual_image_1 = [prefix_et + sat_entity_actual_image_1, sat_entity_actual_image_1, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_actual_image_1])
        new_entity_sat_entity_actual_image_2 = [prefix_et + sat_entity_actual_image_2, sat_entity_actual_image_2, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_actual_image_2])
        new_entity_sat_entity_join = [prefix_et + sat_entity_join, sat_entity_join, ENTITY_WITH, dv_entity.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_join])
        new_entity_sat_entity = [prefix_et + sat_entity, sat_entity, ENTITY_TB, dv_entity.cod_path, 'INSERT', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity])

        has_rs = False
        has_tn = False

        # Test if exists metadata columns only on the first branch. All the branch need to have same columns!
        tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, 1)
        if len(tenant_source) != 0: has_tn = True
        record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, 1)
        if record_source is not None: has_rs = True
        applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, 1)
        if applied_date is not None: has_ad = True

        hash_for_metadata = self.connection.get_hash_for_metadata()
        integer_for_metadata = self.connection.get_integer_for_metadata()

        ########################### Create Entity STG TMP ###########################

        num_branches = self.metadata_actual.get_num_branches_on_entry_dv_from_cod_entity_name(dv_entity.cod_entity)

        for num_branch in range(1, num_branches + 1):

            tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(dv_entity.cod_entity, num_branch)
            if len(tenant_source) != 0:
                has_tn = True
                # Get distinct from TENANTS
                final_tenant_list = []
                for tn in tenant_source:
                    if tn.column_name_target not in [x.column_name_target for x in final_tenant_list]: final_tenant_list.append(tn)
                tenant_source = final_tenant_list

            bk_entry = self.metadata_actual.get_first_entry_dv_mappings_from_cod_entity_target_and_key_type_and_num_branch(sat_cod_entity_target, KEY_TYPE_BUSINESS_KEY, num_branch)

            md5_function = self.get_hash_key_from_cod_entity_target_and_num_branch(sat_cod_entity_target, num_branch)
            new_dataset_mapping = [bk_entry.cod_entity_source, md5_function, prefix_et + sat_entity_tmp,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + sat_entity_tmp,
                                   'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], num_branch, None, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, num_branch)
                new_dataset_mapping = [record_source.cod_entity_source, record_source.column_name_source,
                                       prefix_et + sat_entity_tmp,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                for tn in tenant_source:
                    new_dataset_mapping = [tn.cod_entity_source, tn.column_name_source, prefix_et + sat_entity_tmp,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length,
                                           tn.column_precision,
                                           num_branch, KEY_TYPE_TENANT, 1, self.owner]
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                    ordinal_position += 1

            # Atributes
            applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(dv_entity.cod_entity, num_branch)

            new_dataset_mapping = [applied_date.cod_entity_source, applied_date.column_name_source,
                                   prefix_et + sat_entity_tmp,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            # Hashdiff from applied Date
            md5_function = self.connection.get_md5_function()
            cast_to_string = self.connection.get_cast_string_for_metadata()

            bk_final = cast_to_string.replace('[x]', applied_date.column_name_source)
            hasdiff = md5_function.replace('[x]', bk_final)
            new_dataset_mapping = [applied_date.cod_entity_source, hasdiff,
                                   prefix_et + sat_entity_tmp, 'HASHDIFF',
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   num_branch, KEY_TYPE_ATTRIBUTE, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        ########################### Create Entity STG LAST IMAGE 1 ###########################
        ordinal_position = 1
        new_dataset_mapping = [prefix_et + sat_entity, hash_name, prefix_et + sat_entity_actual_image_1,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity, 'HASHDIFF',
                               prefix_et + sat_entity_actual_image_1, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])


        new_dataset_mapping = [prefix_et + sat_entity, applied_date.column_name_target,
                               prefix_et + sat_entity_actual_image_1,
                               applied_date.column_name_target,
                               applied_date.column_type_target, ordinal_position, applied_date.column_length,
                               applied_date.column_precision,
                               1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        new_dataset_mapping = [prefix_et + sat_entity,
                               'ROW_NUMBER() over (partition by ' + hash_name + ',' + applied_date.column_name_target + ' ORDER BY DATE_CREATED desc)',
                               prefix_et + sat_entity_actual_image_1, 'RN',
                               integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                               integer_for_metadata[2],
                               sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        ########################### Create Entity STG LAST IMAGE 2 ###########################
        ordinal_position = 1
        new_dataset_mapping = [prefix_et + sat_entity_actual_image_1, hash_name,
                               prefix_et + sat_entity_actual_image_2,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_actual_image_1, 'HASHDIFF',
                               prefix_et + sat_entity_actual_image_2, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_actual_image_1, applied_date.column_name_target,
                               prefix_et + sat_entity_actual_image_2,
                               applied_date.column_name_target,
                               applied_date.column_type_target, ordinal_position, applied_date.column_length,
                               applied_date.column_precision,
                               1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        new_filter = [prefix_et + sat_entity_actual_image_2, 'RN = 1', sat_num_branch, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        ########################### Create Entity STG JOIN ###########################
        ordinal_position = 1

        new_dataset_mapping = [prefix_et + sat_entity_tmp, hash_name,
                               prefix_et + sat_entity_join, hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_tmp, 'HASHDIFF',
                               prefix_et + sat_entity_join, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_rs:
            new_dataset_mapping = [prefix_et + sat_entity_tmp, record_source.column_name_target,
                                   prefix_et + sat_entity_join,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   sat_num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + sat_entity_tmp, tn.column_name_target, prefix_et + sat_entity_join,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        new_dataset_mapping = [prefix_et + sat_entity_tmp, 'DATE_CREATED',
                               prefix_et + sat_entity_join, 'DATE_CREATED',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_tmp, applied_date.column_name_target, prefix_et + sat_entity_join,
                               applied_date.column_name_target,
                               applied_date.column_type_target, ordinal_position, applied_date.column_length,
                               applied_date.column_precision,
                               1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        new_dataset_mapping = [prefix_et + sat_entity_actual_image_2, hash_name,
                               prefix_et + sat_entity_join, hash_name + "_HIST",
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_relationship = [prefix_et + sat_entity_tmp, 'HASHDIFF',
                            prefix_et + sat_entity_actual_image_2,
                            'HASHDIFF', "MASTER JOIN", self.owner]
        self.metadata_actual.add_entry_dataset_relationship([new_relationship])
        new_relationship = [prefix_et + sat_entity_tmp, hash_name,
                            prefix_et + sat_entity_actual_image_2,
                            hash_name, "MASTER JOIN", self.owner]
        self.metadata_actual.add_entry_dataset_relationship([new_relationship])

        new_relationship = [prefix_et + sat_entity_tmp, applied_date.column_name_target,
                            prefix_et + sat_entity_actual_image_2,
                            applied_date.column_name_target, "MASTER JOIN", self.owner]
        self.metadata_actual.add_entry_dataset_relationship([new_relationship])

        ########################### Create Entity SAT ###########################
        ordinal_position = 1

        new_dataset_mapping = [prefix_et + sat_entity_join, hash_name,
                               prefix_et + sat_entity, hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_join, 'HASHDIFF',
                               prefix_et + sat_entity, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_rs:
            new_dataset_mapping = [prefix_et + sat_entity_join, record_source.column_name_target,
                                   prefix_et + sat_entity,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   sat_num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + sat_entity_join, tn.column_name_target,
                                       prefix_et + sat_entity,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        new_dataset_mapping = [prefix_et + sat_entity_join, 'DATE_CREATED',
                               prefix_et + sat_entity, 'DATE_CREATED',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])


        new_dataset_mapping = [prefix_et + sat_entity_join, applied_date.column_name_target, prefix_et + sat_entity,
                               applied_date.column_name_target,
                               applied_date.column_type_target, ordinal_position, applied_date.column_length,
                               applied_date.column_precision,
                               1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        new_filter = [prefix_et + sat_entity, hash_name + "_HIST is null", sat_num_branch, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        self.log.log(self.engine_name, "Finished to process Metadata [ Record Tracking Satellite ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_link_creation_link(self, link):
        self.log.log(self.engine_name, "Starting to process Metadata [ Link definition ] information", LOG_LEVEL_ONLY_LOG)
        #TODO: creacion del link -> tener en cuenta si es CDC o no
        ############################################################################################################
        prefix_et = 'ET_'
        has_rs = False
        has_tn = False
        has_ad = False
        has_seq = False
        record_source = None
        tenant_source = None
        seq_source = None
        applied_date = None

        hash_name = 'HASH_' + link.entity_name
        dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(link.cod_entity, 0)
        if dv_property is not None: hash_name = dv_property.hash_name

        # Creation of LINK ENTITY
        ordinal_position = 1
        link_stg_tmp_name = 'STG_TMP_' + link.entity_name
        link_stg_name = 'STG_' + link.entity_name
        link_stg_last_image_name = 'STG_' + link.entity_name + "_LAST_IMAGE"
        link_name = link.entity_name
        new_entity_stg_tmp = [prefix_et + link_stg_tmp_name, link_stg_tmp_name, ENTITY_WITH, link.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_stg_tmp])
        new_entity_stg = [prefix_et + link_stg_name, link_stg_name, ENTITY_WITH, link.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_stg])
        new_entity_stg = [prefix_et + link_stg_last_image_name, link_stg_last_image_name, ENTITY_WITH, link.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_stg])
        new_entity_hub = [prefix_et + link_name, link_name, ENTITY_TB, link.cod_path, "INSERT", self.owner]
        self.metadata_actual.add_entry_entity([new_entity_hub])

        # Include ENTRY from ET_STG_TMP_[Link]
        entry_dv_mapping_bk = []
        num_branches = self.metadata_actual.get_num_branches_on_entry_dv_from_cod_entity_name(link.cod_entity)
        num_connections = self.metadata_actual.get_num_connections_on_entry_dv_from_cod_entity_name(link.cod_entity)

        for num_branch in range(1, num_branches + 1):
            tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(link.cod_entity, num_branch)
            if len(tenant_source) != 0:
                has_tn = True
                # Get distinct from TENANTS
                final_tenant_list = []
                for tn in tenant_source:
                    if tn.column_name_target not in [x.column_name_target for x in final_tenant_list]: final_tenant_list.append(tn)
                tenant_source = final_tenant_list
                tenant_source.sort(key=lambda x: x.ordinal_position)

            seq_source = self.metadata_actual.get_seq_on_dv_from_cod_entity_target_and_num_branch(link.cod_entity, num_branch)
            if len(seq_source) != 0:
                has_seq = True
                seq_source.sort(key=lambda x: x.ordinal_position)

            record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(link.cod_entity, num_branch)
            if record_source is not None: has_rs = True

            applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(link.cod_entity, num_branch)
            if applied_date is not None: has_ad = True

            entry_dv_mapping_bk = self.metadata_actual.get_all_bk_from_entry_dv_cod_entity_target_and_num_branch(link.cod_entity, num_branch)
            entry_dv_mapping_bk.sort(key=lambda x: x.ordinal_position)
            cod_entity_source = entry_dv_mapping_bk[0].cod_entity_source

            md5_function = self.get_hash_key_from_cod_entity_target_and_num_branch(link.cod_entity, num_branch)

            hash_for_metadata = self.connection.get_hash_for_metadata()
            new_dataset_mapping = [cod_entity_source, md5_function, prefix_et + link_stg_tmp_name,
                                   hash_name,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                                   num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
            new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + link_stg_tmp_name, 'DATE_CREATED',
                                   sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                                   sysdate_for_metadata[2], num_branch, KEY_TYPE_NULL, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

            if has_rs:
                new_dataset_mapping = [record_source.cod_entity_source, record_source.column_name_source,
                                       prefix_et + link_stg_tmp_name,
                                       record_source.column_name_target,
                                       record_source.column_type_target, ordinal_position, record_source.column_length,
                                       record_source.column_precision,
                                       num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_ad:
                new_dataset_mapping = [applied_date.cod_entity_source, applied_date.column_name_source,
                                       prefix_et + link_stg_tmp_name,
                                       applied_date.column_name_target,
                                       applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                       applied_date.column_precision,
                                       num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_tn:
                for tn in tenant_source:
                    new_dataset_mapping = [tn.cod_entity_source, tn.column_name_source, prefix_et + link_stg_tmp_name,
                                           tn.column_name_target,
                                           tn.column_type_target, ordinal_position, tn.column_length, tn.column_precision,
                                           num_branch, KEY_TYPE_TENANT, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            if has_seq:
                for seq in seq_source:
                    new_dataset_mapping = [seq.cod_entity_source, seq.column_name_source, prefix_et + link_stg_tmp_name,
                                           seq.column_name_target,
                                           seq.column_type_target, ordinal_position, seq.column_length, seq.column_precision,
                                           num_branch, KEY_TYPE_SEQUENCE, 1, self.owner]
                    ordinal_position += 1
                    self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

            for num_con in range(1, num_connections+1):
                hash_name_hub = 'HASH_' + str(num_con)
                dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(link.cod_entity, num_con)
                if dv_property is not None: hash_name_hub = dv_property.hash_name

                md5_function_for_con = self.get_hash_key_from_cod_entity_target_and_num_branch_and_num_connection(link.cod_entity, num_branch, num_con)
                new_dataset_mapping = [cod_entity_source, md5_function_for_con, prefix_et + link_stg_tmp_name,
                                       hash_name_hub,
                                       hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                       hash_for_metadata[2],
                                       num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])


        # Relationship on STG_TMP and LINK
        ordinal_position = 1
        new_relationship = [prefix_et + link_stg_tmp_name, hash_name, prefix_et + link_name,
                            hash_name, 'MASTER JOIN', self.owner]
        self.metadata_actual.add_entry_dataset_relationship([new_relationship])


        # STG
        hash_for_metadata = self.connection.get_hash_for_metadata()
        new_dataset_mapping = [prefix_et + link_stg_tmp_name, hash_name, prefix_et + link_stg_name,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2], 1,
                               KEY_TYPE_HASH_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        new_dataset_mapping = [prefix_et + link_name, hash_name, prefix_et + link_stg_name,
                               hash_name + "_LINK",
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2], 1,
                               KEY_TYPE_HASH_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = [prefix_et + link_stg_tmp_name, 'DATE_CREATED', prefix_et + link_stg_name, 'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], 1, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [prefix_et + link_stg_tmp_name,
                                   record_source.column_name_target,
                                   prefix_et + link_stg_name,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [prefix_et + link_stg_tmp_name,
                                   applied_date.column_name_target,
                                   prefix_et + link_stg_name,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + link_stg_tmp_name, tn.column_name_target, prefix_et + link_stg_name,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_seq:
            for seq in seq_source:
                new_dataset_mapping = [prefix_et + link_stg_tmp_name, seq.column_name_target, prefix_et + link_stg_name,
                                       seq.column_name_target,
                                       seq.column_type_target, ordinal_position, seq.column_length,
                                       seq.column_precision,
                                       1, KEY_TYPE_SEQUENCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        for num_con in range(1, num_connections + 1):
            hash_name_hub = 'HASH_' + str(num_con)
            dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(link.cod_entity, num_con)
            if dv_property is not None: hash_name_hub = dv_property.hash_name

            new_dataset_mapping = [prefix_et + link_stg_tmp_name, hash_name_hub, prefix_et + link_stg_name,
                                   hash_name_hub,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])


        # Filter
        new_filter = [prefix_et + link_stg_last_image_name, hash_name + "_LINK is null", 1, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])




        ############################# Last image #############################
        ordinal_position = 1
        hash_for_metadata = self.connection.get_hash_for_metadata()
        new_dataset_mapping = [prefix_et + link_stg_name, hash_name, prefix_et + link_stg_last_image_name,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2], 1,
                               KEY_TYPE_HASH_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = [prefix_et + link_stg_name, 'DATE_CREATED', prefix_et + link_stg_last_image_name, 'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], 1, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [prefix_et + link_stg_name,
                                   record_source.column_name_target,
                                   prefix_et + link_stg_last_image_name,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [prefix_et + link_stg_name,
                                   applied_date.column_name_target,
                                   prefix_et + link_stg_last_image_name,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + link_stg_name, tn.column_name_target, prefix_et + link_stg_last_image_name,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        if has_seq:
            for seq in seq_source:
                new_dataset_mapping = [prefix_et + link_stg_name, seq.column_name_target, prefix_et + link_stg_last_image_name,
                                       seq.column_name_target,
                                       seq.column_type_target, ordinal_position, seq.column_length,
                                       seq.column_precision,
                                       1, KEY_TYPE_SEQUENCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        for num_con in range(1, num_connections + 1):
            hash_name_hub = 'HASH_' + str(num_con)
            dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(link.cod_entity, num_con)
            if dv_property is not None: hash_name_hub = dv_property.hash_name
            new_dataset_mapping = [prefix_et + link_stg_name, hash_name_hub, prefix_et + link_stg_last_image_name,
                                   hash_name_hub,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        integer_for_metadata = self.connection.get_integer_for_metadata()
        date_for_last_image = 'DATE_CREATED'
        if has_ad: date_for_last_image = applied_date.column_name_target
        new_dataset_mapping = [prefix_et + link_stg_name,
                               'ROW_NUMBER() over (partition by ' + hash_name + ' ORDER BY ' + date_for_last_image + ' desc)',
                               prefix_et + link_stg_last_image_name, 'RN',
                               integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                               integer_for_metadata[2],
                               1, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        ############################ Final LINK ##########################

        ordinal_position = 1
        hash_for_metadata = self.connection.get_hash_for_metadata()
        new_dataset_mapping = [prefix_et + link_stg_last_image_name, hash_name, prefix_et + link_name,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2], 1,
                               KEY_TYPE_HASH_KEY, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = [prefix_et + link_stg_last_image_name, 'DATE_CREATED', prefix_et + link_name, 'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], 1, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [prefix_et + link_stg_last_image_name,
                                   record_source.column_name_target,
                                   prefix_et + link_name,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   1, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [prefix_et + link_stg_last_image_name,
                                   applied_date.column_name_target,
                                   prefix_et + link_name,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   1, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + link_stg_last_image_name, tn.column_name_target, prefix_et + link_name,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        if has_seq:
            for seq in seq_source:
                new_dataset_mapping = [prefix_et + link_stg_last_image_name, seq.column_name_target,
                                       prefix_et + link_name,
                                       seq.column_name_target,
                                       seq.column_type_target, ordinal_position, seq.column_length,
                                       seq.column_precision,
                                       1, KEY_TYPE_SEQUENCE, 1, self.owner]
                ordinal_position += 1
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        for num_con in range(1, num_connections + 1):
            hash_name_hub = 'HASH_' + str(num_con)
            dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(link.cod_entity,
                                                                                                    num_con)
            if dv_property is not None: hash_name_hub = dv_property.hash_name
            new_dataset_mapping = [prefix_et + link_stg_last_image_name, hash_name_hub, prefix_et + link_name,
                                   hash_name_hub,
                                   hash_for_metadata[0], ordinal_position, hash_for_metadata[1],
                                   hash_for_metadata[2],
                                   1, KEY_TYPE_HASH_KEY, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_filter = [prefix_et + link_name, "RN = 1", 1, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        self.log.log(self.engine_name, "Finished to process Metadata [ Link definition ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_link_creation_sat(self, link):
        self.log.log(self.engine_name, "Starting to process Metadata [ Link satellites ] information", LOG_LEVEL_ONLY_LOG)
        all_satellites = self.metadata_actual.get_all_satellites_info_from_hub(link.cod_entity)
        # SAT: cod_entity_source | cod_entity_target | satellite_name | num_branch | origin_is_incremental | origin_is_total | origin_is_cdc
        for sat in all_satellites:
            if int(sat[6]) == 0:
                self.process_dv_link_creation_sat_non_cdc(link, sat)
            elif int(sat[6]) == 1:
                self.process_dv_link_creation_sat_cdc(link, sat)

        self.log.log(self.engine_name, "Finished to process Metadata [ Link satellites ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_link_creation_sat_non_cdc(self, link, sat):
        self.log.log(self.engine_name, "Starting to process Metadata [ Link satellites - non cdc ] information", LOG_LEVEL_ONLY_LOG)

        ordinal_position = 1
        prefix_et = 'ET_'
        sat_cod_entity_source = sat[0]
        sat_cod_entity_target = sat[1]
        sat_name = sat[2]
        sat_num_branch = 1 # Sat can't have more than one branch -> sat[3]

        hash_name = 'HASH_' + link.entity_name
        dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(link.cod_entity, 0)
        if dv_property is not None: hash_name = dv_property.hash_name

        ########################### Create all entities ###########################
        sat_entity_tmp = 'STG_TMP_' + sat_name
        sat_entity_actual_image_1 = 'STG_TMP_LAST_IMAGE_1_' + sat_name
        sat_entity_actual_image_2 = 'STG_TMP_LAST_IMAGE_2_' + sat_name
        sat_entity_join = 'STG_TMP_JOIN_' + sat_name
        sat_entity = sat_name

        new_entity_sat_entity_tmp = [prefix_et + sat_entity_tmp, sat_entity_tmp, ENTITY_WITH, link.cod_path, '',
                                     self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_tmp])
        new_entity_sat_entity_actual_image_1 = [prefix_et + sat_entity_actual_image_1, sat_entity_actual_image_1,
                                                ENTITY_WITH, link.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_actual_image_1])
        new_entity_sat_entity_actual_image_2 = [prefix_et + sat_entity_actual_image_2, sat_entity_actual_image_2,
                                                ENTITY_WITH, link.cod_path, '', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_actual_image_2])
        new_entity_sat_entity_join = [prefix_et + sat_entity_join, sat_entity_join, ENTITY_WITH, link.cod_path, '',
                                      self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_join])
        new_entity_sat_entity = [prefix_et + sat_entity, sat_entity, ENTITY_TB, link.cod_path, 'INSERT', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity])

        has_rs = False
        has_tn = False
        has_ad = False
        has_dck = False
        record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat_num_branch)
        if record_source is not None: has_rs = True
        tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat_num_branch)
        if len(tenant_source) != 0:
            has_tn = True
            # Get distinct from TENANTS
            final_tenant_list = []
            for tn in tenant_source:
                if tn.column_name_target not in [x.column_name_target for x in
                                                 final_tenant_list]: final_tenant_list.append(tn)
            tenant_source = final_tenant_list
        dependent_child_key = self.metadata_actual.get_dependent_child_key_on_dv_from_satellite_name(sat_name)
        if len(dependent_child_key) != 0: has_dck = True
        applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(link.cod_entity, sat[3])
        if applied_date is not None: has_ad = True

        hash_for_metadata = self.connection.get_hash_for_metadata()
        integer_for_metadata = self.connection.get_integer_for_metadata()

        ########################### Create Entity STG TMP ###########################
        md5_function = self.get_hash_key_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat[3])
        hash_md5_function = md5_function
        new_dataset_mapping = [sat_cod_entity_source, md5_function, prefix_et + sat_entity_tmp,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + sat_entity_tmp,
                               'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [sat_cod_entity_source, record_source.column_name_source,
                                   prefix_et + sat_entity_tmp,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   sat_num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [sat_cod_entity_source, applied_date.column_name_source,
                                   prefix_et + sat_entity_tmp,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   sat_num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [sat_cod_entity_source, tn.column_name_source, prefix_et + sat_entity_tmp,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        all_dck_concatenate = ''
        if has_dck:
            for dck in dependent_child_key:
                all_dck_concatenate += ", " + dck.column_name_source
                new_dataset_mapping = [sat_cod_entity_source, dck.column_name_source, prefix_et + sat_entity_tmp,
                                       dck.column_name_target,
                                       dck.column_type_target, ordinal_position, dck.column_length,
                                       dck.column_precision,
                                       1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        all_attributes = self.metadata_actual.get_attributes_on_dv_from_satellite_name(sat_entity)

        for at in all_attributes:
            new_dataset_mapping = [at.cod_entity_source, at.column_name_source,
                                   prefix_et + sat_entity_tmp,
                                   at.column_name_target,
                                   at.column_type_target, ordinal_position, at.column_length,
                                   at.column_precision,
                                   sat_num_branch, at.key_type, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        md5_function = self.connection.get_md5_function()
        cast_to_string = self.connection.get_cast_string_for_metadata()

        bk_concatenate = ''
        at_cod_entity_source = ''
        for at in all_attributes:
            bk_final = cast_to_string.replace('[x]', at.column_name_source)
            bk_concatenate += bk_final + "||'" + self.module_dv_char_separator_naming + "'||"
        bk_concatenate = bk_concatenate[:-6 - len(self.module_dv_char_separator_naming)]
        hasdiff = md5_function.replace('[x]', bk_concatenate)
        new_dataset_mapping = [all_attributes[0].cod_entity_source, hasdiff,
                               prefix_et + sat_entity_tmp, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        order_by = ''
        if has_ad:
            order_by = ' order by ' + applied_date.column_name_source + ' desc'
        if has_dck:
            hash_md5_function += all_dck_concatenate
        new_dataset_mapping = [sat_cod_entity_source,
                               'ROW_NUMBER() over (partition by ' + hash_md5_function + order_by + ' )',
                               prefix_et + sat_entity_tmp, 'RN',
                               integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                               integer_for_metadata[2],
                               sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        ########################### Create Entity STG LAST IMAGE 1 ###########################
        ordinal_position = 1
        new_dataset_mapping = [prefix_et + sat_entity, hash_name, prefix_et + sat_entity_actual_image_1,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity, 'HASHDIFF',
                               prefix_et + sat_entity_actual_image_1, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        all_dck_concatenate = ''
        if has_dck:
            for dck in dependent_child_key:
                all_dck_concatenate += "," + dck.column_name_target
                new_dataset_mapping = [prefix_et + sat_entity, dck.column_name_target,
                                       prefix_et + sat_entity_actual_image_1,
                                       dck.column_name_target,
                                       dck.column_type_target, ordinal_position, dck.column_length,
                                       dck.column_precision,
                                       1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        new_dataset_mapping = [prefix_et + sat_entity,
                               'ROW_NUMBER() over (partition by ' + hash_name + ' ' + all_dck_concatenate + ' ORDER BY DATE_CREATED desc)',
                               prefix_et + sat_entity_actual_image_1, 'RN',
                               integer_for_metadata[0], ordinal_position, integer_for_metadata[1],
                               integer_for_metadata[2],
                               sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        ########################### Create Entity STG LAST IMAGE 2 ###########################
        ordinal_position = 1
        new_dataset_mapping = [prefix_et + sat_entity_actual_image_1, hash_name,
                               prefix_et + sat_entity_actual_image_2,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_actual_image_1, 'HASHDIFF',
                               prefix_et + sat_entity_actual_image_2, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_dck:
            for dck in dependent_child_key:
                new_dataset_mapping = [prefix_et + sat_entity_actual_image_1, dck.column_name_target,
                                       prefix_et + sat_entity_actual_image_2,
                                       dck.column_name_target,
                                       dck.column_type_target, ordinal_position, dck.column_length,
                                       dck.column_precision,
                                       1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        new_filter = [prefix_et + sat_entity_actual_image_2, 'RN = 1', sat_num_branch, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        ########################### Create Entity STG JOIN ###########################
        ordinal_position = 1

        new_dataset_mapping = [prefix_et + sat_entity_tmp, hash_name,
                               prefix_et + sat_entity_join, hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_tmp, 'HASHDIFF',
                               prefix_et + sat_entity_join, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_rs:
            new_dataset_mapping = [prefix_et + sat_entity_tmp, record_source.column_name_target,
                                   prefix_et + sat_entity_join,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   sat_num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [prefix_et + sat_entity_tmp, applied_date.column_name_target,
                                   prefix_et + sat_entity_join,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   sat_num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])


        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + sat_entity_tmp, tn.column_name_target, prefix_et + sat_entity_join,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        new_dataset_mapping = [prefix_et + sat_entity_tmp, 'DATE_CREATED',
                               prefix_et + sat_entity_join, 'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1], sysdate_for_metadata[2],
                               sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_dck:
            for dck in dependent_child_key:
                new_dataset_mapping = [prefix_et + sat_entity_tmp, dck.column_name_target, prefix_et + sat_entity_join,
                                       dck.column_name_target,
                                       dck.column_type_target, ordinal_position, dck.column_length,
                                       dck.column_precision,
                                       1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        for at in all_attributes:
            new_dataset_mapping = [prefix_et + sat_entity_tmp, at.column_name_target,
                                   prefix_et + sat_entity_join,
                                   at.column_name_target,
                                   at.column_type_target, ordinal_position, at.column_length,
                                   at.column_precision,
                                   sat_num_branch, at.key_type, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        new_dataset_mapping = [prefix_et + sat_entity_actual_image_2, hash_name,
                               prefix_et + sat_entity_join, hash_name + "_HIST",
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_relationship = [prefix_et + sat_entity_tmp, 'HASHDIFF',
                            prefix_et + sat_entity_actual_image_2,
                            'HASHDIFF', "MASTER JOIN", self.owner]
        self.metadata_actual.add_entry_dataset_relationship([new_relationship])
        new_relationship = [prefix_et + sat_entity_tmp, hash_name,
                            prefix_et + sat_entity_actual_image_2,
                            hash_name, "MASTER JOIN", self.owner]
        self.metadata_actual.add_entry_dataset_relationship([new_relationship])
        if has_dck:
            for dck in dependent_child_key:
                new_relationship = [prefix_et + sat_entity_tmp, dck.column_name_target,
                                    prefix_et + sat_entity_actual_image_2,
                                    dck.column_name_target, "MASTER JOIN", self.owner]
                self.metadata_actual.add_entry_dataset_relationship([new_relationship])

        new_filter = [prefix_et + sat_entity_join, 'RN = 1', sat_num_branch, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        ########################### Create Entity SAT ###########################
        ordinal_position = 1

        new_dataset_mapping = [prefix_et + sat_entity_join, hash_name,
                               prefix_et + sat_entity, hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        new_dataset_mapping = [prefix_et + sat_entity_join, 'HASHDIFF',
                               prefix_et + sat_entity, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_rs:
            new_dataset_mapping = [prefix_et + sat_entity_join, record_source.column_name_target,
                                   prefix_et + sat_entity,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   sat_num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [prefix_et + sat_entity_join, applied_date.column_name_target,
                                   prefix_et + sat_entity,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   sat_num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [prefix_et + sat_entity_join, tn.column_name_target,
                                       prefix_et + sat_entity,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        new_dataset_mapping = [prefix_et + sat_entity_join, 'DATE_CREATED',
                               prefix_et + sat_entity, 'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1], sysdate_for_metadata[2],
                               sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_dck:
            for dck in dependent_child_key:
                new_dataset_mapping = [prefix_et + sat_entity_join, dck.column_name_target, prefix_et + sat_entity,
                                       dck.column_name_target,
                                       dck.column_type_target, ordinal_position, dck.column_length,
                                       dck.column_precision,
                                       1, KEY_TYPE_DEPENDENT_CHILD_KEY, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        for at in all_attributes:
            new_dataset_mapping = [prefix_et + sat_entity_join, at.column_name_target,
                                   prefix_et + sat_entity,
                                   at.column_name_target,
                                   at.column_type_target, ordinal_position, at.column_length,
                                   at.column_precision,
                                   sat_num_branch, at.key_type, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        new_filter = [prefix_et + sat_entity, hash_name + "_HIST is null", sat_num_branch, self.owner]
        self.metadata_actual.add_entry_filters([new_filter])

        self.log.log(self.engine_name, "Finished to process Metadata [ Link satellites - non cdc ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_link_creation_sat_cdc(self, link, sat):
        self.log.log(self.engine_name, "Starting to process Metadata [ Link satellites - cdc ] information", LOG_LEVEL_ONLY_LOG)
        ordinal_position = 1
        prefix_et = 'ET_'
        sat_cod_entity_source = sat[0]
        sat_cod_entity_target = sat[1]
        sat_name = sat[2]
        sat_num_branch = 1 # Sat can't have more than one branch -> sat[3]
        sat_entity = sat_name

        hash_name = 'HASH_' + link.entity_name
        dv_property = self.metadata_actual.get_dv_properties_from_cod_entity_and_num_connection(link.cod_entity, 0)
        if dv_property is not None: hash_name = dv_property.hash_name

        new_entity_sat_entity_tmp = [prefix_et + sat_entity, sat_entity, ENTITY_TB, link.cod_path, 'INSERT', self.owner]
        self.metadata_actual.add_entry_entity([new_entity_sat_entity_tmp])

        has_rs = False
        has_tn = False
        has_ad = False
        tenant_source = self.metadata_actual.get_tenant_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat_num_branch)
        if len(tenant_source) != 0:
            has_tn = True
            # Get distinct from TENANTS
            final_tenant_list = []
            for tn in tenant_source:
                if tn.column_name_target not in [x.column_name_target for x in
                                                 final_tenant_list]: final_tenant_list.append(tn)
            tenant_source = final_tenant_list
        record_source = self.metadata_actual.get_record_source_on_dv_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat_num_branch)
        if record_source is not None: has_rs = True
        applied_date = self.metadata_actual.get_applied_date_on_dv_from_cod_entity_target(link.cod_entity, sat[3])
        if applied_date is not None: has_ad = True

        hash_for_metadata = self.connection.get_hash_for_metadata()
        md5_function = self.get_hash_key_from_cod_entity_target_and_num_branch(sat_cod_entity_target, sat[3])

        new_dataset_mapping = [sat_cod_entity_source, md5_function, prefix_et + sat_entity,
                               hash_name,
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASH_KEY, 1, self.owner]
        ordinal_position += 1
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        sysdate_for_metadata = self.connection.get_sysdate_for_metadata()
        new_dataset_mapping = ['', self.connection.get_sysdate_value(), prefix_et + sat_entity,
                               'DATE_CREATED',
                               sysdate_for_metadata[0], ordinal_position, sysdate_for_metadata[1],
                               sysdate_for_metadata[2], sat_num_branch, KEY_TYPE_NULL, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
        ordinal_position += 1

        if has_rs:
            new_dataset_mapping = [sat_cod_entity_source, record_source.column_name_source,
                                   prefix_et + sat_entity,
                                   record_source.column_name_target,
                                   record_source.column_type_target, ordinal_position, record_source.column_length,
                                   record_source.column_precision,
                                   sat_num_branch, KEY_TYPE_RECORD_SOURCE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_ad:
            new_dataset_mapping = [sat_cod_entity_source, applied_date.column_name_source,
                                   prefix_et + sat_entity,
                                   applied_date.column_name_target,
                                   applied_date.column_type_target, ordinal_position, applied_date.column_length,
                                   applied_date.column_precision,
                                   sat_num_branch, KEY_TYPE_APPLIED_DATE, 1, self.owner]
            ordinal_position += 1
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        if has_tn:
            for tn in tenant_source:
                new_dataset_mapping = [sat_cod_entity_source, tn.column_name_source, prefix_et + sat_entity,
                                       tn.column_name_target,
                                       tn.column_type_target, ordinal_position, tn.column_length,
                                       tn.column_precision,
                                       1, KEY_TYPE_TENANT, 1, self.owner]
                self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
                ordinal_position += 1

        all_attributes = self.metadata_actual.get_attributes_on_dv_from_satellite_name(sat_entity)

        for at in all_attributes:
            new_dataset_mapping = [at.cod_entity_source, at.column_name_source,
                                   prefix_et + sat_entity,
                                   at.column_name_target,
                                   at.column_type_target, ordinal_position, at.column_length,
                                   at.column_precision,
                                   sat_num_branch, at.key_type, 1, self.owner]
            self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])
            ordinal_position += 1

        md5_function = self.connection.get_md5_function()
        cast_to_string = self.connection.get_cast_string_for_metadata()

        bk_concatenate = ''
        for at in all_attributes:
            bk_final = cast_to_string.replace('[x]', at.column_name_source)
            bk_concatenate += bk_final + "||'" + self.module_dv_char_separator_naming + "'||"
        bk_concatenate = bk_concatenate[:-2]
        hasdiff = md5_function.replace('[x]', bk_concatenate)
        new_dataset_mapping = [all_attributes[0].cod_entity_source, hasdiff,
                               prefix_et + sat_entity, 'HASHDIFF',
                               hash_for_metadata[0], ordinal_position, hash_for_metadata[1], hash_for_metadata[2],
                               sat_num_branch, KEY_TYPE_HASHDIFF, 1, self.owner]
        self.metadata_actual.add_entry_dataset_mappings([new_dataset_mapping])

        self.log.log(self.engine_name, "Finished to process Metadata [ Link satellites - cdc ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv_properties(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ DV Properties ] information", LOG_LEVEL_ONLY_LOG)
        all_entities = []
        for entry in [x for x in self.metadata_actual.entry_dv_entity]:
            new_entity = [entry.entity_name, entry.entity_type]
            if new_entity not in all_entities: all_entities.append(new_entity)
        for entry in [x for x in self.metadata_actual.entry_dv_entity]:
            if entry.name_status_tracking_satellite is None or entry.name_status_tracking_satellite=='': continue
            new_entity = [entry.name_status_tracking_satellite, ENTITY_STS]
            if new_entity not in all_entities: all_entities.append(new_entity)
        for entry in [x for x in self.metadata_actual.entry_dv_entity]:
            if entry.name_record_tracking_satellite is None or entry.name_record_tracking_satellite == '': continue
            new_entity = [entry.name_record_tracking_satellite, ENTITY_RTS]
            if new_entity not in all_entities: all_entities.append(new_entity)
        for entry in [x for x in self.metadata_actual.entry_dv_entity]:
            if entry.name_effectivity_satellite is None or entry.name_effectivity_satellite == '': continue
            new_entity = [entry.name_effectivity_satellite, ENTITY_SATE]
            if new_entity not in all_entities: all_entities.append(new_entity)
        for entry in [x for x in self.metadata_actual.entry_dv_mappings]:
            if entry.satellite_name is None or entry.satellite_name == '': continue
            new_entity = [entry.satellite_name, ENTITY_SAT]
            if new_entity not in all_entities: all_entities.append(new_entity)

        dataset_added = []
        for entry in all_entities:
            new_dataset_id = self.metadata_to_load.get_dataset_from_dataset_name(entry[0]).id_dataset
            id_entity_type = self.metadata_actual.get_entity_type_from_entity_type_name(entry[1]).id_entity_type

            old_dataset_dv = self.metadata_actual.get_dataset_dv_from_id_dataset(new_dataset_id)

            if old_dataset_dv is None:
                new_dataset_dv = [new_dataset_id, id_entity_type, self.owner,
                                         self.connection_metadata.get_sysdate_value(), "NULL"]
                self.metadata_to_load.add_om_dataset_dv([new_dataset_dv])
                dataset_added.append(new_dataset_id)
            else:
                if old_dataset_dv.id_entity_type == id_entity_type:
                    new_dataset_dv = [old_dataset_dv.id_dataset, old_dataset_dv.id_entity_type,
                                                  self.owner, "'" + str(old_dataset_dv.start_date) + "'", "NULL"]
                    self.metadata_to_load.add_om_dataset_dv([new_dataset_dv])
                    dataset_added.append(old_dataset_dv.id_dataset)
                else:
                    new_dataset_dv = [old_dataset_dv.id_dataset, old_dataset_dv.id_entity_type,
                                                  self.owner, "'" + str(old_dataset_dv.start_date) + "'",
                                                  self.connection_metadata.get_sysdate_value()]
                    self.metadata_to_load.add_om_dataset_dv([new_dataset_dv])

                    new_dataset_dv = [new_dataset_id, id_entity_type, self.owner,
                                             self.connection_metadata.get_sysdate_value(), "NULL"]
                    self.metadata_to_load.add_om_dataset_dv([new_dataset_dv])
                    dataset_added.append(new_dataset_id)

        for dataset_dv in [x for x in self.metadata_actual.om_dataset_dv if x.end_date is None]:
            if dataset_dv.id_dataset not in dataset_added:

                not_arriving_dataset_execution = [dataset_dv.id_dataset, dataset_dv.id_entity_type,
                                                  self.owner, "'" + str(dataset_dv.start_date) + "'",
                                                  self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_dv([not_arriving_dataset_execution])

        self.log.log(self.engine_name, "Finished to process Metadata [ DV Properties ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_sources(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Sources ] information", LOG_LEVEL_ONLY_LOG)
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
                if len(table_definition) == 0: self.log.log(self.engine_name,
                                                            "Source [ '" + entity.table_name + "' ] is not created in the database.",
                                                            LOG_LEVEL_WARNING)

                # Source Specification
                if dataset is None:
                    # If the dataset is new, all the dataset specification will be added
                    for table_definition_spec in table_definition:
                        id_dataset_spec = next_id_dataset_spec
                        next_id_dataset_spec += 1
                        id_key_type = (self.metadata_actual.get_key_type_from_key_type_name(table_definition_spec.key_type)).id_key_type
                        start_date = self.connection_metadata.get_sysdate_value()
                        end_date = "NULL"

                        new_dataset_specification = [id_dataset_spec, id_dataset, id_key_type,
                                                     table_definition_spec.column_name,
                                                     table_definition_spec.column_type, table_definition_spec.id,
                                                     table_definition_spec.is_nullable, table_definition_spec.column_length,
                                                     table_definition_spec.column_precision, table_definition_spec.column_scale,
                                                     self.owner, start_date, end_date]
                        self.metadata_to_load.add_om_dataset_specification([new_dataset_specification])
                        sources_specs_loaded.append([id_dataset, table_definition_spec.column_name])

                else:
                    # Source specification existent
                    # Update any column
                    for existent_col in [x for x in self.metadata_actual.om_dataset_specification if x.id_dataset == dataset.id_dataset and x.end_date is None]:
                        finded = False
                        for table_definition_spec in table_definition:
                            id_key_type = (self.metadata_actual.get_key_type_from_key_type_name(table_definition_spec.key_type)).id_key_type

                            checksum_existent = str(
                                existent_col.id_key_type) + existent_col.column_name + existent_col.column_type + \
                                                str(existent_col.ordinal_position) + str(
                                existent_col.is_nullable) + str(existent_col.column_length) + \
                                                str(existent_col.column_precision) + str(existent_col.column_scale)
                            checksum_new = str(
                                id_key_type) + table_definition_spec.column_name + table_definition_spec.column_type + \
                                           str(table_definition_spec.id) + str(table_definition_spec.is_nullable) + str(
                                table_definition_spec.column_length) + \
                                           str(table_definition_spec.column_precision) + str(table_definition_spec.column_scale)
                            if checksum_new == checksum_existent:
                                finded = True
                                # Column that exists already, if on origin is the same, we maintain all the info
                                close_dataset_specification = [existent_col.id_dataset_spec, dataset.id_dataset,
                                                               existent_col.id_key_type,
                                                               existent_col.column_name,
                                                               existent_col.column_type,
                                                               existent_col.ordinal_position, existent_col.is_nullable,
                                                               existent_col.column_length,
                                                               existent_col.column_precision, existent_col.column_scale,
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
                                                           existent_col.column_length,
                                                           existent_col.column_precision, existent_col.column_scale,
                                                           existent_col.meta_owner,
                                                           "'" + str(existent_col.start_date) + "'",
                                                           self.connection_metadata.get_sysdate_value()]
                            self.metadata_to_load.add_om_dataset_specification([close_dataset_specification])
                            sources_specs_loaded.append([existent_col.id_dataset, existent_col.column_name])

                    # Add new columns
                    for table_definition_spec in table_definition:
                        finded = False
                        for existent_col in [x for x in self.metadata_actual.om_dataset_specification if x.id_dataset == dataset.id_dataset and x.end_date is None]:
                            id_key_type = (
                                self.metadata_actual.get_key_type_from_key_type_name(table_definition_spec.key_type)).id_key_type

                            checksum_existent = str(
                                existent_col.id_key_type) + existent_col.column_name + existent_col.column_type + \
                                                str(existent_col.ordinal_position) + str(
                                existent_col.is_nullable) + str(existent_col.column_length) + \
                                                str(existent_col.column_precision) + str(existent_col.column_scale)
                            checksum_new = str(
                                id_key_type) + table_definition_spec.column_name + table_definition_spec.column_type + \
                                           str(table_definition_spec.id) + str(table_definition_spec.is_nullable) + str(
                                table_definition_spec.column_length) + \
                                           str(table_definition_spec.column_precision) + str(table_definition_spec.column_scale)
                            if checksum_new == checksum_existent:
                                finded = True
                                break
                        # New column is added on source
                        if not finded:
                            id_dataset_spec = next_id_dataset_spec
                            next_id_dataset_spec += 1
                            id_key_type = (
                                self.metadata_actual.get_key_type_from_key_type_name(table_definition_spec.key_type)).id_key_type
                            start_date = self.connection_metadata.get_sysdate_value()
                            end_date = "NULL"

                            new_dataset_specification = [id_dataset_spec, dataset.id_dataset, id_key_type,
                                                         table_definition_spec.column_name,
                                                         table_definition_spec.column_type, table_definition_spec.id,
                                                         table_definition_spec.is_nullable,
                                                         table_definition_spec.column_length,
                                                         table_definition_spec.column_precision, table_definition_spec.column_scale,
                                                         self.owner, start_date, end_date]
                            self.metadata_to_load.add_om_dataset_specification([new_dataset_specification])
                            sources_specs_loaded.append([dataset.id_dataset, table_definition_spec.column_name])

        # Close sources that not arrive anymore
        for dataset in [x for x in self.metadata_actual.om_dataset if x.id_entity_type == self.metadata_actual.get_entity_type_from_entity_type_name(ENTITY_SRC).id_entity_type]:
            if dataset.dataset_name not in sources_loaded and dataset.end_date is None:
                close_source = [dataset.id_dataset, dataset.dataset_name, dataset.id_entity_type,
                                dataset.id_path, dataset.meta_owner, "'" + str(dataset.start_date) + "'",
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
                            and self.metadata_actual.get_entity_type_from_entity_type_name(entity.entity_type).id_entity_type == dataset.id_entity_type:
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

                table_definition = self.metadata_actual.get_cols_from_cod_entity_on_entry(entity.cod_entity)
                # Source Specification
                if dataset is None:
                    # New Sources Specification
                    for table_definition_spec in table_definition:
                        id_dataset_spec = next_id_dataset_spec
                        next_id_dataset_spec += 1
                        id_key_type = (self.metadata_actual.get_key_type_from_key_type_name(table_definition_spec.key_type)).id_key_type
                        start_date = self.connection_metadata.get_sysdate_value()
                        end_date = "NULL"

                        new_dataset_specification = [id_dataset_spec, id_dataset, id_key_type,
                                                     table_definition_spec.column_name,
                                                     table_definition_spec.column_type, table_definition_spec.id,
                                                     table_definition_spec.is_nullable, table_definition_spec.column_length,
                                                     table_definition_spec.column_precision, table_definition_spec.column_scale,
                                                     self.owner, start_date, end_date]
                        self.metadata_to_load.add_om_dataset_specification([new_dataset_specification])
                        tmp_specs_loaded.append([id_dataset, table_definition_spec.column_name])

                else:
                    # Source specification existent
                    # Update any column
                    for existent_col in [x for x in self.metadata_actual.om_dataset_specification if x.id_dataset == dataset.id_dataset and x.end_date is None]:
                        finded = False
                        for table_definition_spec in table_definition:
                            id_key_type = (self.metadata_actual.get_key_type_from_key_type_name(table_definition_spec.key_type)).id_key_type

                            checksum_existent = str(
                                existent_col.id_key_type) + existent_col.column_name + existent_col.column_type + \
                                                str(existent_col.ordinal_position) + str(
                                existent_col.is_nullable) + str(existent_col.column_length) + \
                                                str(existent_col.column_precision) + str(existent_col.column_scale)
                            checksum_new = str(
                                id_key_type) + table_definition_spec.column_name + table_definition_spec.column_type + \
                                           str(table_definition_spec.id) + str(table_definition_spec.is_nullable) + str(
                                table_definition_spec.column_length) + str(table_definition_spec.column_precision) + str(
                                table_definition_spec.column_scale)
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
                                                               existent_col.column_length,
                                                               existent_col.column_precision, existent_col.column_scale,
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
                                                           existent_col.column_length,
                                                           existent_col.column_precision, existent_col.column_scale,
                                                           existent_col.meta_owner,
                                                           "'" + str(existent_col.start_date) + "'",
                                                           self.connection_metadata.get_sysdate_value()]
                            self.metadata_to_load.add_om_dataset_specification([close_dataset_specification])
                            tmp_specs_loaded.append([existent_col.id_dataset, existent_col.column_name])

                    # Add new columns
                    for table_definition_spec in table_definition:
                        finded = False
                        for existent_col in [x for x in self.metadata_actual.om_dataset_specification if x.id_dataset == dataset.id_dataset and x.end_date is None]:
                            id_key_type = (
                                self.metadata_actual.get_key_type_from_key_type_name(table_definition_spec.key_type)).id_key_type

                            checksum_existent = str(
                                existent_col.id_key_type) + existent_col.column_name + existent_col.column_type + \
                                                str(existent_col.ordinal_position) + str(
                                existent_col.is_nullable) + str(existent_col.column_length) + \
                                                str(existent_col.column_precision) + str(existent_col.column_scale)
                            checksum_new = str(
                                id_key_type) + table_definition_spec.column_name + table_definition_spec.column_type + \
                                           str(table_definition_spec.id) + str(table_definition_spec.is_nullable) + str(
                                table_definition_spec.column_length) + \
                                           str(table_definition_spec.column_precision) + str(table_definition_spec.column_scale)
                            if checksum_new == checksum_existent:
                                finded = True
                                break
                        # New column is added on source
                        if not finded:
                            id_dataset_spec = next_id_dataset_spec
                            next_id_dataset_spec += 1
                            id_key_type = (
                                self.metadata_actual.get_key_type_from_key_type_name(table_definition_spec.key_type)).id_key_type
                            start_date = self.connection_metadata.get_sysdate_value()
                            end_date = "NULL"

                            new_dataset_specification = [id_dataset_spec, dataset.id_dataset, id_key_type,
                                                         table_definition_spec.column_name,
                                                         table_definition_spec.column_type,
                                                         table_definition_spec.id,
                                                         table_definition_spec.is_nullable,
                                                         table_definition_spec.column_length,
                                                         table_definition_spec.column_precision, table_definition_spec.column_scale,
                                                         self.owner, start_date, end_date]
                            self.metadata_to_load.add_om_dataset_specification([new_dataset_specification])
                            tmp_specs_loaded.append([dataset.id_dataset, table_definition_spec.column_name])

        # Close tables that not arrive anymore
        for dataset in [x for x in self.metadata_actual.om_dataset
                        if x.id_entity_type == self.metadata_actual.get_entity_type_from_entity_type_name(ENTITY_TB).id_entity_type
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
                                      dataset_spec.is_nullable, dataset_spec.column_length,
                                      dataset_spec.column_precision,
                                      dataset_spec.column_scale, dataset_spec.meta_owner,
                                      "'" + str(dataset_spec.start_date) + "'", self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_specification([close_dataset_spec])

        self.next_id_dataset = next_id_dataset
        self.next_id_dataset_spec = next_id_dataset_spec

        self.log.log(self.engine_name, "Finished to process Metadata [ Sources ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_order(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Order ] information", LOG_LEVEL_ONLY_LOG)
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

        self.log.log(self.engine_name, "Finished to process Metadata [ Order ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_files(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Files ] information", LOG_LEVEL_ONLY_LOG)
        ######################## LOAD ORDER ########################
        # Input Orders
        files_loaded = []
        for file in self.metadata_actual.entry_files:

            dataset = self.metadata_to_load.get_dataset_from_dataset_name(self.metadata_actual.get_table_name_from_cod_entity_on_entry(file.cod_entity))

            dataset_file_existent = self.metadata_actual.get_om_dataset_file_from_id_dataset(dataset.id_dataset)

            if dataset_file_existent is None:
                # New file
                start_date = self.connection_metadata.get_sysdate_value()
                new_file = [dataset.id_dataset, file.file_path, file.file_name, file.delimiter_character,
                            self.owner, start_date, 'NULL']
                self.metadata_to_load.add_om_dataset_file([new_file])
                files_loaded.append([dataset.id_dataset, file.file_path, file.file_name, file.delimiter_character])

            else:
                # Update file only
                # if the attributes are the diferent, the register will be closed
                if dataset_file_existent.file_path == file.file_path \
                        and dataset_file_existent.file_name == file.file_name \
                        and dataset_file_existent.delimiter_character == file.delimiter_character:
                    same_file = [dataset_file_existent.id_dataset, dataset_file_existent.file_path,
                                 dataset_file_existent.file_name, dataset_file_existent.delimiter_character,
                                 dataset_file_existent.meta_owner,
                                 "'" + str(dataset_file_existent.start_date) + "'", "NULL"]
                    self.metadata_to_load.add_om_dataset_file([same_file])
                    files_loaded.append([dataset_file_existent.id_dataset, dataset_file_existent.file_path, dataset_file_existent.file_name, dataset_file_existent.delimiter_character])
                else:
                    close_file = [dataset_file_existent.id_dataset, dataset_file_existent.file_path,
                                 dataset_file_existent.file_name, dataset_file_existent.delimiter_character, dataset_file_existent.meta_owner,
                                   "'" + str(dataset_file_existent.start_date) + "'", self.connection_metadata.get_sysdate_value()]
                    self.metadata_to_load.add_om_dataset_file([close_file])
                    files_loaded.append([dataset_file_existent.id_dataset, dataset_file_existent.file_path, dataset_file_existent.file_name, dataset_file_existent.delimiter_character])

                    new_file = [dataset.id_dataset, file.file_path, file.file_name, file.delimiter_character,
                                 self.owner, self.connection_metadata.get_sysdate_value(), "NULL"]
                    self.metadata_to_load.add_om_dataset_file([new_file])
                    files_loaded.append([dataset.id_dataset, file.file_path, file.file_name, file.delimiter_character])

        # Close order that not arrive anymore
        for file in [x for x in self.metadata_actual.om_dataset_file if x.end_date is None]:
            if [file.id_dataset, file.file_path, file.file_name, file.delimiter_character] not in files_loaded:
                close_file = [file.id_dataset, file.file_path, file.file_name, file.delimiter_character,
                               file.meta_owner, "'" + str(file.start_date) + "'",
                               self.connection_metadata.get_sysdate_value()]
                self.metadata_to_load.add_om_dataset_file([close_file])

        self.log.log(self.engine_name, "Finished to process Metadata [ Files ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_relationship(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Relationship ] information", LOG_LEVEL_ONLY_LOG)

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

        self.log.log(self.engine_name, "Finished to process Metadata [ Relationship ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_aggregator(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Aggregator ] information", LOG_LEVEL_ONLY_LOG)

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

        self.log.log(self.engine_name, "Finished to process Metadata [ Aggregator ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_distinct(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Distinct ] information", LOG_LEVEL_ONLY_LOG)
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

        self.log.log(self.engine_name, "Finished to process Metadata [ Distinct ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_mapping(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Mapping ] information", LOG_LEVEL_ONLY_LOG)
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
                if re.search(r"\b" + col + r"\b", value_mapping) or re.search(r"(^" + col + "$)", value_mapping):
                    dataset_spec_source = self.metadata_to_load.get_dataset_spec_from_id_dataset_and_column_name(dataset_source.id_dataset, col)
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

        self.log.log(self.engine_name, "Finished to process Metadata [ Mapping ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_filter(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Filter ] information", LOG_LEVEL_ONLY_LOG)
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
                all_columns_from_source = self.metadata_to_load.get_all_columns_from_table_name(dataset_source.dataset_name)
                for col in all_columns_from_source:
                    if re.search(r"(\s+|\(|^)"+col+"(\s+|\)|$)", value_mapping):
                        dataset_spec_source = self.metadata_to_load.get_dataset_spec_from_id_dataset_and_column_name(dataset_source.id_dataset, col)
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

        self.log.log(self.engine_name, "Finished to process Metadata [ Filter ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_having(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Having ] information", LOG_LEVEL_ONLY_LOG)
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
                    if re.search(r"\b" + col + "\b", value_having) or re.search(r"(^" + col + "$)", value_having):
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

        self.log.log(self.engine_name, "Finished to process Metadata [ Having ] information", LOG_LEVEL_ONLY_LOG)

    def process_elt_historical(self):
        self.log.log(self.engine_name, "Starting to process Metadata [ Historical ] information", LOG_LEVEL_ONLY_LOG)

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
                                                                 closed_col.column_length,
                                                                 closed_col.column_precision, closed_col.column_scale,
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
                , distinct.meta_owner, "'" + str(distinct.start_date) + "'", "'" + str(distinct.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_t_distinct([close_distinct])

        for mapping in [x for x in self.metadata_actual.om_dataset_t_mapping if x.end_date is not None]:
            close_mapping = [mapping.id_t_mapping, mapping.id_branch,
                             mapping.id_dataset_spec, mapping.value_mapping,
                             mapping.meta_owner, "'" + str(mapping.start_date) + "'", "'" + str(mapping.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_t_mapping([close_mapping])

        for filter in [x for x in self.metadata_actual.om_dataset_t_filter if x.end_date is not None]:
            close_filter = [filter.id_t_filter, filter.id_dataset,
                            filter.id_branch,
                            filter.value_filter, filter.meta_owner,
                            "'" + str(filter.start_date) + "'", "'" + str(filter.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_t_filter([close_filter])

        for having in [x for x in self.metadata_actual.om_dataset_t_having if x.end_date is not None]:
            close_having = [having.id_t_having, having.id_dataset,
                            having.id_branch,
                            having.value_having, having.meta_owner,
                            "'" + str(having.start_date) + "'", "'" + str(having.end_date) + "'"]
            self.metadata_to_load.add_om_dataset_t_having([close_having])

        for execution in [x for x in self.metadata_actual.om_dataset_execution if x.end_date is not None]:

            close_execution = [execution.id_dataset, execution.id_query_type, execution.meta_owner,
                               "'" +str(execution.start_date)+ "'", "'" +str(execution.end_date)+ "'"]
            self.metadata_to_load.add_om_dataset_execution([close_execution])

        for dataset_dv in [x for x in self.metadata_actual.om_dataset_dv if x.end_date is not None]:

            close_dataset_dv = [dataset_dv.id_dataset, dataset_dv.id_entity_type, dataset_dv.meta_owner,
                               "'" +str(dataset_dv.start_date)+ "'", "'" +str(dataset_dv.end_date)+ "'"]
            self.metadata_to_load.add_om_dataset_dv([close_dataset_dv])

        self.log.log(self.engine_name, "Finished to process Metadata [ Historical ] information", LOG_LEVEL_ONLY_LOG)

    def process_dv(self):
        self.log.log(self.engine_name, "Starting to process Metadata from DV Module", LOG_LEVEL_INFO)

        self.process_dv_hub()
        self.process_dv_link()

        self.log.log(self.engine_name, "Finished to process Metadata from DV Module", LOG_LEVEL_INFO)

    def process_dv_final(self):
        self.log.log(self.engine_name, "Starting to process Metadata DV [ end phase ]", LOG_LEVEL_INFO)

        self.process_dv_properties()

        self.log.log(self.engine_name, "Finished to process Metadata DV [ end phase ]", LOG_LEVEL_INFO)

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

        # OM_DATASET_DV
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_DV)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_DV)
        query.set_insert_columns(COLUMNS_OM_DATASET_DV)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_dv)
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

        # OM_DATASET_FILE
        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_DELETE)
        query.set_target_table(TABLE_OM_DATASET_FILE)
        query.set_where_filters(where_filter_owner)
        connection.execute(str(query))

        query = Query()
        query.set_database(connection_type)
        query.set_values_batch(commit_values_batch)
        query.set_type(QUERY_TYPE_VALUES)
        query.set_target_table(TABLE_OM_DATASET_FILE)
        query.set_insert_columns(COLUMNS_OM_DATASET_FILE)
        query.set_has_header(False)
        query.set_values(self.metadata_to_load.om_dataset_file)
        connection.execute(str(query))

        connection.commit()
        connection.close()

        self.log.log(self.engine_name, "Uploading completed", LOG_LEVEL_INFO)
