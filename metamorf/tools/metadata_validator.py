from metamorf.constants import *
from metamorf.tools.log import Log
from metamorf.tools.utils import is_valid_table_name, is_valid_column_name


class MetadataValidator:

    def __init__(self, metadata, source_connection, configuration, log):
        self.metadata = metadata
        self.log = log
        self.validator_name = 'Metadata Validator'
        self.configuration = configuration
        self.connection = source_connection

        self.initialize_references()
        '''
        How to obtain table columns
        variable_connection = self.configuration_file['data']['connection_type'].lower() + "_database"
        configuration_connection_data = self.configuration_file['data']
        configuration_connection_data[variable_connection] = (self.metadata_to_load.get_path_from_id_path(id_path)).database_name
        self.connection.setup_connection(configuration_connection_data, self.log)
        table_definition = self.connection.get_table_columns_definition(entity.table_name)'''

    def initialize_references(self):
        self.all_entity_type = []
        for x in self.metadata.om_ref_entity_type: self.all_entity_type.append(x.entity_type_name)
        self.all_join_type = []
        for x in self.metadata.om_ref_join_type: self.all_join_type.append(x.join_name)
        self.all_key_type = []
        for x in self.metadata.om_ref_key_type: self.all_key_type.append(x.key_type_name)
        self.all_order_type = []
        for x in self.metadata.om_ref_order_type: self.all_order_type.append(x.order_type_name)
        self.all_query_type = []
        for x in self.metadata.om_ref_query_type: self.all_query_type.append(x.query_type_name)

        self.all_cod_path = []
        self.all_cod_entity_elt = []
        self.all_cod_entity_elt_detail = dict()

    def validate_metadata(self):
        self.log.log(self.validator_name, 'Starting Metadata Entry Validation', LOG_LEVEL_INFO)
        result = self.validate_metadata_entry_path()
        result = result and self.validate_metadata_entry_entity()
        result = result and self.validate_metadata_entry_dataset_mappings()
        result = result and self.validate_metadata_entry_aggregators()
        result = result and self.validate_metadata_entry_filters()
        result = result and self.validate_metadata_entry_having()
        result = result and self.validate_metadata_entry_order()
        result = result and self.validate_metadata_entry_files()
        result = result and self.validate_metadata_entry_dataset_relationships()
        result = result and self.validate_metadata_entry_elt()
        result = result and self.validate_metadata_entry_dv_entity()
        result = result and self.validate_metadata_entry_dv_properties()
        result = result and self.validate_metadata_entry_dv_mappings()
        result = result and self.validate_metadata_entry_datavault()

        self.log.log(self.validator_name, 'Metadata Entry Validation finished', LOG_LEVEL_INFO)
        return result

    def validate_metadata_entry_path(self):
        table_validation = 'ENTRY_PATH'
        self.log.log(self.validator_name, 'Start metadata validation on [ '+table_validation+' ]', LOG_LEVEL_DEBUG)
        result = True
        special_characters = '!@#$%^&*()-+?=,<>/.'
        for path in self.metadata.entry_path:
            if path.cod_path is None or path.cod_path == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_PATH ] can not be null', LOG_LEVEL_ERROR)
            if path.owner is None or path.owner == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ OWNER ] can not be null', LOG_LEVEL_ERROR)
            if any(c in special_characters for c in path.database_name):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ DATABASE_NAME ] only accepts alphanumeric characters', LOG_LEVEL_ERROR)
            if any(c in special_characters for c in str(path.schema_name)):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ SCHEMA_NAME ] only accepts alphanumeric characters', LOG_LEVEL_ERROR)
            if path.database_name is None or path.database_name == '':
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ DATABASE_NAME ] null value', LOG_LEVEL_WARNING)
            if path.schema_name is None or path.schema_name == '':
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ SCHEMA_NAME ] null value', LOG_LEVEL_WARNING)
            if path.cod_path not in self.all_cod_path: self.all_cod_path.append(path.cod_path)

        # PostgreSQL: Cross-database references are not allowed
        if self.connection.get_connection_type() == CONNECTION_POSTGRESQL:
            database_postgre = None
            for path in self.metadata.entry_path:
                if database_postgre is None: database_postgre = path.database_name
                if database_postgre != path.database_name:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ DATABASE_NAME ] on PostgreSQL, the database needs to be the same for all the paths, cross-database references are not allowed', LOG_LEVEL_ERROR)

        if self.connection.get_connection_type() == CONNECTION_SQLITE:
            for path in self.metadata.entry_path:
                if path.database_name != 'MAIN':
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ DATABASE_NAME ] on SQLite, the database needs to be MAIN', LOG_LEVEL_ERROR)
                if path.schema_name != '' and path.schema_name is not None:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ SCHEMA_NAME ] on SQLite must be null', LOG_LEVEL_ERROR)

        if self.connection.get_connection_type() == CONNECTION_MYSQL:
            for path in self.metadata.entry_path:
                if path.schema_name != '' and path.schema_name is not None:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ SCHEMA_NAME ] on MySQL must be null', LOG_LEVEL_ERROR)

        self.log.log(self.validator_name, 'Finished metadata validation on [ '+table_validation+' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_entity(self):
        table_validation = 'ENTRY_ENTITY'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        for entity in self.metadata.entry_entity:
            if entity.cod_entity is None or entity.cod_entity == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY ] can not be null', LOG_LEVEL_ERROR)
            if not is_valid_table_name(entity.cod_entity):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_ENTITY ] invalid name', LOG_LEVEL_ERROR)
            if entity.table_name is None or entity.table_name == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ TABLE_NAME ] can not be null', LOG_LEVEL_ERROR)
            if entity.entity_type is None or entity.entity_type == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ ENTITY_TYPE ] can not be null', LOG_LEVEL_ERROR)
            if entity.entity_type not in self.all_entity_type:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ ENTITY_TYPE ] invalid value', LOG_LEVEL_ERROR)
            if entity.cod_path is None or entity.cod_path == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_PATH ] can not be null', LOG_LEVEL_ERROR)
            if entity.cod_path not in self.all_cod_path:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_PATH ] invalid value', LOG_LEVEL_ERROR)
            if entity.strategy not in self.all_query_type and entity.strategy != '' and entity.strategy is not None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_STRATEGY ] invalid value', LOG_LEVEL_ERROR)
            if entity.owner is None or entity.owner == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ OWNER ] can not be null', LOG_LEVEL_ERROR)
            if entity.cod_entity in self.all_cod_entity_elt:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_ENTITY ] already exists, it must be unique', LOG_LEVEL_ERROR)
            if not is_valid_table_name(entity.table_name):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ TABLE_NAME ] invalid name', LOG_LEVEL_ERROR)

            if entity.cod_entity not in self.all_cod_entity_elt: self.all_cod_entity_elt.append(entity.cod_entity)

            # Add Column to Entity
            if entity.cod_entity not in self.all_cod_entity_elt_detail:
                self.all_cod_entity_elt_detail[entity.cod_entity] = dict()
                self.all_cod_entity_elt_detail[entity.cod_entity]['type'] = entity.entity_type
                self.all_cod_entity_elt_detail[entity.cod_entity]['columns'] = []

        self.log.log(self.validator_name, 'Finished metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_dataset_mappings(self):
        table_validation = 'ENTRY_DATASET_MAPPINGS'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        all_entities_by_branch = dict()

        for entry in self.metadata.entry_dataset_mappings:
            if entry.cod_entity_source not in self.all_cod_entity_elt and entry.cod_entity_source is not None and entry.cod_entity_source != '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_SOURCE ] invalid value', LOG_LEVEL_ERROR)
            if entry.cod_entity_source is None or entry.cod_entity_source == '':
                self.log.log(self.validator_name,
                             'Metadata Entry [ ' + table_validation + ' ] -> [ COD_ENTITY_SOURCE ] null value',
                             LOG_LEVEL_WARNING)
            if entry.value_source is None or entry.value_source == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ VALUE_SOURCE ] can not be null', LOG_LEVEL_ERROR)
            if entry.cod_entity_target not in self.all_cod_entity_elt and entry.cod_entity_target is not None and entry.cod_entity_target != '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_TARGET ] invalid value', LOG_LEVEL_ERROR)
            if entry.column_name_target is None or entry.column_name_target == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_NAME_TARGET ] can not be null', LOG_LEVEL_ERROR)
            if entry.column_type_target is None or entry.column_type_target == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_TYPE_TARGET ] can not be null', LOG_LEVEL_ERROR)
            if entry.ordinal_position is None or entry.ordinal_position == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ ORDINAL_POSITION ] can not be null', LOG_LEVEL_ERROR)
            if entry.column_length is None or entry.column_length == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_LENGTH ] can not be null', LOG_LEVEL_ERROR)
            if entry.column_precision is None or entry.column_precision == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_PRECISION ] can not be null', LOG_LEVEL_ERROR)
            if entry.num_branch is None or entry.num_branch == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ NUM_BRANCH ] can not be null', LOG_LEVEL_ERROR)
            if entry.key_type not in KEY_TYPE_ELT:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ KEY_TYPE ] invalid value', LOG_LEVEL_ERROR)
            if entry.sw_distinct is None or entry.sw_distinct == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ SW_DISTINCT ] can not be null', LOG_LEVEL_ERROR)
            if entry.owner is None or entry.owner == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ OWNER ] can not be null', LOG_LEVEL_ERROR)

            if entry.ordinal_position < 1:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ ORDINAL_POSITION ] needs to be positive', LOG_LEVEL_ERROR)

            if entry.column_length < 0:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_LENGTH ] needs to be positive', LOG_LEVEL_ERROR)

            if entry.column_precision < 0:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_PRECISION ] needs to be positive', LOG_LEVEL_ERROR)

            if entry.sw_distinct not in [0,1]:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+ table_validation + ' ] -> [ SW_DISTINCT ] only accepts 0/1 values', LOG_LEVEL_ERROR)

            if entry.column_type_target.upper() not in self.connection.get_data_types():
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_TYPE_TARGET ] is not a valid type', LOG_LEVEL_ERROR)

            if not is_valid_column_name(entry.column_name_target):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_NAME_TARGET ] invalid name', LOG_LEVEL_ERROR)

            # Validation: all the branches has the same number of rows
            if entry.cod_entity_target in all_entities_by_branch:
                if entry.num_branch in all_entities_by_branch[entry.cod_entity_target]:
                    all_entities_by_branch[entry.cod_entity_target][entry.num_branch] = all_entities_by_branch[entry.cod_entity_target][entry.num_branch] +1
                else:
                    all_entities_by_branch[entry.cod_entity_target][entry.num_branch] = 1
            else:
                all_entities_by_branch[entry.cod_entity_target] = dict()
                all_entities_by_branch[entry.cod_entity_target][entry.num_branch] = 1

            # Add Column to Entity
            if entry.cod_entity_target not in self.all_cod_entity_elt_detail:
                self.all_cod_entity_elt_detail[entry.cod_entity_target] = dict()
                self.all_cod_entity_elt_detail[entry.cod_entity_target]['columns'] = []
                self.all_cod_entity_elt_detail[entry.cod_entity_target]['columns'].append(entry.column_name_target.upper())
            else:
                if entry.column_name_target not in self.all_cod_entity_elt_detail[entry.cod_entity_target]['columns']:
                    self.all_cod_entity_elt_detail[entry.cod_entity_target]['columns'].append(entry.column_name_target.upper())

        # Validation: all the branches are consecutive
        for x in all_entities_by_branch.items():
            start_branch = 1
            for y in x[1].items():
                if start_branch != y[0]:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> Num branches form entity [' + x[0] + '] are not consecutive from 0', LOG_LEVEL_ERROR)
                start_branch += 1

        # Validation: all the branches has the same number of rows
        for x in all_entities_by_branch.items():
            num_records_by_branch = 0
            for y in x[1].items():
                if num_records_by_branch != y[1] and num_records_by_branch != 0:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> Num branches not equal', LOG_LEVEL_ERROR)
                num_records_by_branch = y[1]

        self.log.log(self.validator_name, 'Finished metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_aggregators(self):
        table_validation = 'ENTRY_AGGREGATORS'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        for agg in self.metadata.entry_aggregators:
            if agg.cod_entity_target == '' or agg.cod_entity_target is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_TARGET ] can not be null', LOG_LEVEL_ERROR)
            if agg.cod_entity_src == '' or agg.cod_entity_src is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_SOURCE ] can not be null', LOG_LEVEL_ERROR)
            if agg.cod_entity_target not in self.all_cod_entity_elt:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_TARGET ] doesn\'t exist on ENTRY_ENTITY', LOG_LEVEL_ERROR)
            if agg.cod_entity_src not in self.all_cod_entity_elt:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_SOURCE ] doesn\'t exist on ENTRY_ENTITY', LOG_LEVEL_ERROR)
            if agg.column_name == '' or agg.column_name is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_NAME ] can not be null', LOG_LEVEL_ERROR)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_filters(self):
        table_validation = 'ENTRY_FILTERS'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        for agg in self.metadata.entry_filters:
            if agg.cod_entity_target == '' or agg.cod_entity_target is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_TARGET ] can not be null', LOG_LEVEL_ERROR)
            if agg.value == '' or agg.value is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ VALUE ] can not be null', LOG_LEVEL_ERROR)
            if agg.num_branch == '' or agg.num_branch is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ NUM_BRANCH ] can not be null', LOG_LEVEL_ERROR)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_having(self):
        table_validation = 'ENTRY_HAVING'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        for hav in self.metadata.entry_having:
            if hav.cod_entity_target == '' or hav.cod_entity_target is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_TARGET ] can not be null', LOG_LEVEL_ERROR)
            if hav.value == '' or hav.value is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ VALUE ] can not be null', LOG_LEVEL_ERROR)
            if hav.num_branch == '' or hav.num_branch is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ NUM_BRANCH ] can not be null', LOG_LEVEL_ERROR)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_order(self):
        table_validation = 'ENTRY_ORDER'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        #TODO: añadir validación de existencia
        for ord in self.metadata.entry_order:
            if ord.cod_entity_target == '' or ord.cod_entity_target is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_TARGET ] can not be null', LOG_LEVEL_ERROR)
            if ord.cod_entity_src == '' or ord.cod_entity_src is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_SOURCE ] can not be null', LOG_LEVEL_ERROR)
            if ord.column_name == '' or ord.column_name is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_NAME ] can not be null', LOG_LEVEL_ERROR)
            if ord.order_type == '' or ord.order_type is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ ORDER_TYPE ] can not be null', LOG_LEVEL_ERROR)
            if ord.num_branch == '' or ord.num_branch is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ NUM_BRANCH ] can not be null', LOG_LEVEL_ERROR)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_files(self):
        table_validation = 'ENTRY_FILES'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        for fil in self.metadata.entry_files:
            if fil.cod_entity == '' or fil.cod_entity is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY ] can not be null', LOG_LEVEL_ERROR)
            if fil.file_path == '' or fil.file_path is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ FILE_PATH ] can not be null', LOG_LEVEL_ERROR)
            if fil.file_name == '' or fil.file_name is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ FILE_NAME ] can not be null', LOG_LEVEL_ERROR)
            if fil.delimiter_character == '' or fil.delimiter_character is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ DELIMITER_CHARACTER ] can not be null', LOG_LEVEL_ERROR)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_dataset_relationships(self):
        table_validation = 'ENTRY_DATASET_RELATIONSHIPS'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        for dat in self.metadata.entry_dataset_relationship:
            if dat.cod_entity_master == '' or dat.cod_entity_master is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_MASTER ] can not be null', LOG_LEVEL_ERROR)
            if dat.cod_entity_detail == '' or dat.cod_entity_detail is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_DETAIL ] can not be null', LOG_LEVEL_ERROR)
            if dat.column_name_master == '' or dat.column_name_master is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_NAME_MASTER ] can not be null', LOG_LEVEL_ERROR)
            if dat.column_name_detail == '' or dat.column_name_detail is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_NAME_DETAIL ] can not be null', LOG_LEVEL_ERROR)
            if dat.relationship_type == '' or dat.relationship_type is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ RELATIONSHIP_TYPE ] can not be null', LOG_LEVEL_ERROR)
            if dat.relationship_type not in self.all_join_type:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ RELATIONSHIP_TYPE ] has not a valid value', LOG_LEVEL_ERROR)
            if dat.cod_entity_master not in self.all_cod_entity_elt:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_ENTITY_MASTER ] has not a valid value, not setted on ENTRY_ENTITY', LOG_LEVEL_ERROR)
            if dat.cod_entity_detail not in self.all_cod_entity_elt:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_ENTITY_DETAIL ] has not a valid value, not setted on ENTRY_ENTITY', LOG_LEVEL_ERROR)
            if self.all_cod_entity_elt_detail[dat.cod_entity_master]['type'] != 'SRC' and dat.column_name_master.upper() not in self.all_cod_entity_elt_detail[dat.cod_entity_master]['columns']:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_NAME_MASTER ] has not a valid value, not calculated on DATASET_MAPPINGS', LOG_LEVEL_ERROR)
            if self.all_cod_entity_elt_detail[dat.cod_entity_detail]['type'] != 'SRC' and dat.column_name_detail.upper() not in self.all_cod_entity_elt_detail[dat.cod_entity_detail]['columns']:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_NAME_DETAIL ] has not a valid value, not calculated on DATASET_MAPPINGS', LOG_LEVEL_ERROR)
            if self.all_cod_entity_elt_detail[dat.cod_entity_detail]['type'] == 'SRC':
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_NAME_DETAIL ] no validation is performed, before execution the source must exist in the database', LOG_LEVEL_WARNING)
            if self.all_cod_entity_elt_detail[dat.cod_entity_master]['type'] == 'SRC':
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_NAME_MASTER ] no validation is performed, before execution the source must exist in the database', LOG_LEVEL_WARNING)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_elt(self):
        table_validation = 'ELT'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        # Validate DELETE Strategy has defined a Primary Key
        for dat in self.metadata.entry_entity:
            if dat.strategy == 'DELETE' or dat.strategy == "MERGE" or dat.strategy == "UPDATE":
                have_pk = False
                for map in self.metadata.entry_dataset_mappings:
                    if map.key_type == KEY_TYPE_PRIMARY_KEY and map.cod_entity_target == dat.cod_entity:
                        have_pk = True
                if not have_pk:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ '+dat.strategy.upper() +' Strategy ] need to have a Primary Key', LOG_LEVEL_ERROR)

        for entity in self.all_cod_entity_elt_detail:
            if self.all_cod_entity_elt_detail[entity]['type']=='SRC': continue
            if len(self.all_cod_entity_elt_detail[entity]['columns']) == 0:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> Entity not defined on Dataset Mappings', LOG_LEVEL_ERROR)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_dv_entity(self):
        table_validation = 'ENTRY_DV_ENTITY'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        for dat in self.metadata.entry_dv_entity:
            if dat.cod_entity == '' or dat.cod_entity is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY ] can not be null', LOG_LEVEL_ERROR)
            if dat.entity_name == '' or dat.entity_name is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ ENTITY_NAME ] can not be null', LOG_LEVEL_ERROR)
            if dat.entity_type == '' or dat.entity_type is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ ENTITY_TYPE ] can not be null', LOG_LEVEL_ERROR)
            if dat.cod_path == '' or dat.cod_path is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_PATH ] can not be null', LOG_LEVEL_ERROR)
            if dat.cod_path not in self.all_cod_path:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_PATH ] invalid value', LOG_LEVEL_ERROR)
            if dat.entity_type not in ['HUB', 'LINK']:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ ENTITY_TYPE ] invalid value', LOG_LEVEL_ERROR)
            if dat.cod_entity in self.all_cod_entity_elt:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_ENTITY ] already exists, it must be unique', LOG_LEVEL_ERROR)
            if not is_valid_table_name(dat.name_status_tracking_satellite) and dat.name_status_tracking_satellite != '' and dat.name_status_tracking_satellite is not None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ NAME_STATUS_TRACKING_SATELLITE ] invalid name', LOG_LEVEL_ERROR)
            if not is_valid_table_name(dat.name_record_tracking_satellite) and dat.name_record_tracking_satellite != '' and dat.name_record_tracking_satellite is not None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ NAME_RECORD_TRACKING_SATELLITE ] invalid name', LOG_LEVEL_ERROR)
            if not is_valid_table_name(dat.name_effectivity_satellite) and dat.name_effectivity_satellite != '' and dat.name_effectivity_satellite is not None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ NAME_EFFECTIVITY_SATELLITE ] invalid name', LOG_LEVEL_ERROR)
            if not is_valid_table_name(dat.entity_name):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ ENTITY_NAME ] invalid name', LOG_LEVEL_ERROR)
            if not is_valid_table_name(dat.cod_entity):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_ENTITY ] invalid name', LOG_LEVEL_ERROR)

            if dat.cod_entity not in self.all_cod_entity_elt: self.all_cod_entity_elt.append(dat.cod_entity)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_dv_properties(self):
        table_validation = 'ENTRY_DV_PROPERTIES'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        for dat in self.metadata.entry_dv_properties:
            if dat.cod_entity == '' or dat.cod_entity is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY ] can not be null', LOG_LEVEL_ERROR)
            if dat.cod_entity not in self.all_cod_entity_elt:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_ENTITY ] invalid value', LOG_LEVEL_ERROR)
            if dat.num_connection == '' or dat.num_connection is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ NUM_CONNECTION ] can not be null', LOG_LEVEL_ERROR)
            if dat.hash_name == '' or dat.hash_name is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ HASH_NAME ] can not be null', LOG_LEVEL_ERROR)
            if not is_valid_column_name(dat.hash_name):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ HASH_NAME ] invalid name', LOG_LEVEL_ERROR)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_dv_mappings(self):
        table_validation = 'ENTRY_DV_MAPPINGS'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        all_entities_by_branch = dict()
        all_satellites = dict()
        all_ordinal_position_same_col_same_pos = dict()
        all_ordinal_position_dif_pos = dict()
        all_sources_origin_type = dict()
        row_by_pk = []

        for dat in self.metadata.entry_dv_mappings:
            if dat.cod_entity_source == '' or dat.cod_entity_source is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_SOURCE ] can not be null', LOG_LEVEL_ERROR)
            if dat.cod_entity_source not in self.all_cod_entity_elt:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_ENTITY ] invalid value', LOG_LEVEL_ERROR)
            if dat.cod_entity_target == '' or dat.cod_entity_target is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COD_ENTITY_TARGET ] can not be null', LOG_LEVEL_ERROR)
            if dat.cod_entity_target not in self.all_cod_entity_elt:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COD_ENTITY_TARGET ] invalid value', LOG_LEVEL_ERROR)
            if dat.column_name_target == '' or dat.column_name_target is None:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_NAME_TARGET ] can not be null', LOG_LEVEL_ERROR)
            if not is_valid_column_name(dat.column_name_target):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_NAME_TARGET ] invalid name', LOG_LEVEL_ERROR)
            if dat.column_type_target.upper() not in self.connection.get_data_types():
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_TYPE_TARGET ] is not a valid type', LOG_LEVEL_ERROR)
            if dat.ordinal_position is None or dat.ordinal_position == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ ORDINAL_POSITION ] can not be null', LOG_LEVEL_ERROR)
            if int(dat.ordinal_position) < 1:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ ORDINAL_POSITION ] needs to be positive', LOG_LEVEL_ERROR)
            if dat.column_length is None or dat.column_length == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_LENGTH ] can not be null', LOG_LEVEL_ERROR)
            if dat.column_length < 0:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_LENGTH ] needs to be positive', LOG_LEVEL_ERROR)
            if dat.column_precision is None or dat.column_precision == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ COLUMN_PRECISION ] can not be null', LOG_LEVEL_ERROR)
            if int(dat.column_precision) < 0:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ COLUMN_PRECISION ] needs to be positive', LOG_LEVEL_ERROR)
            if dat.num_branch is None or dat.num_branch == '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+table_validation+' ] -> [ NUM_BRANCH ] can not be null', LOG_LEVEL_ERROR)
            if dat.num_branch < 0:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ NUM_BRANCH ] needs to be positive', LOG_LEVEL_ERROR)
            if dat.key_type not in KEY_TYPE_DATAVAULT and (dat.satellite_name is None or dat.satellite_name == ''):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ KEY_TYPE ] invalid value', LOG_LEVEL_ERROR)
            if dat.key_type not in KEY_TYPE_DATAVAULT_SATELLITE and dat.satellite_name is not None and dat.satellite_name != '':
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ KEY_TYPE ] invalid value', LOG_LEVEL_ERROR)
            if dat.satellite_name is not None and not is_valid_table_name(dat.satellite_name):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ SATELLITE_NAME ] invalid name', LOG_LEVEL_ERROR)
            if dat.origin_is_incremental not in [0,1]:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ ORIGIN_IS_INCREMENTAL ] invalid value', LOG_LEVEL_ERROR)
            if dat.origin_is_total not in [0,1]:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ ORIGIN_IS_TOTAL ] invalid value', LOG_LEVEL_ERROR)
            if dat.origin_is_cdc not in [0,1]:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ ORIGIN_IS_CDC ] invalid value', LOG_LEVEL_ERROR)

            # Validation: satellite can only be set on connection 0
            if dat.satellite_name != '' and dat.satellite_name is not None and dat.num_connection != 0:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ NUM_CONNECTION ] is always setted to 0 when SATELLITE_NAME is specified', LOG_LEVEL_ERROR)

            # Validation: all the branches has the same number of rows
            if dat.cod_entity_target in all_entities_by_branch:
                if dat.num_branch in all_entities_by_branch[dat.cod_entity_target]:
                    all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['num_items'] = all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['num_items'] + 1
                else:
                    all_entities_by_branch[dat.cod_entity_target][dat.num_branch] = dict()
                    all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['num_items'] = 1
                    all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['bk'] = 0
                    all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['rs'] = 0
                    all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['tn'] = 0
                    all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['seq'] = 0
                    all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['ad'] = 0
                    all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['num_connection'] = 0
                    all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['dk'] = 0
            else:
                all_entities_by_branch[dat.cod_entity_target] = dict()
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch] = dict()
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['num_items'] = 1
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['bk'] = 0
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['rs'] = 0
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['tn'] = 0
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['seq'] = 0
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['ad'] = 0
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['num_connection'] = 0
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['dk'] = 0

            if dat.key_type == 'BK':
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['bk'] =  all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['bk'] + 1
            if dat.key_type == 'RS':
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['rs'] =  all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['rs'] + 1
            if dat.key_type == 'TN':
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['tn'] =  all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['tn'] + 1
            if dat.key_type == 'SEQ':
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['seq'] =  all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['seq'] + 1
            if dat.key_type == 'AD':
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['ad'] =  all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['ad'] + 1
            if dat.key_type == 'DK':
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['dk'] =  all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['dk'] + 1
            if dat.num_connection > all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['num_connection']:
                all_entities_by_branch[dat.cod_entity_target][dat.num_branch]['num_connection'] = dat.num_connection

            # Validation: One satellite can have only one source
            if dat.satellite_name != '' and dat.satellite_name is not None:
                if dat.satellite_name not in all_satellites:
                    all_satellites[dat.satellite_name] = dat.cod_entity_source + "|" + str(dat.num_branch)
                else:
                    if (dat.cod_entity_source + "|" + str(dat.num_branch)) != all_satellites[dat.satellite_name]:
                        result = False
                        self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ SATELLITE_NAME ] can only be loaded by one source', LOG_LEVEL_ERROR)
            if dat.cod_entity_source not in all_sources_origin_type:
                all_sources_origin_type[dat.cod_entity_source] = dict()
                all_sources_origin_type[dat.cod_entity_source]['incremental'] = 0
                all_sources_origin_type[dat.cod_entity_source]['total'] = 0
                all_sources_origin_type[dat.cod_entity_source]['cdc'] = 0
            else:
                if dat.origin_is_incremental:
                    all_sources_origin_type[dat.cod_entity_source]['incremental'] = all_sources_origin_type[dat.cod_entity_source]['incremental'] + 1
                if dat.origin_is_total:
                    all_sources_origin_type[dat.cod_entity_source]['total'] = all_sources_origin_type[dat.cod_entity_source]['total'] + 1
                if dat.origin_is_cdc:
                    all_sources_origin_type[dat.cod_entity_source]['cdc'] = all_sources_origin_type[dat.cod_entity_source]['cdc'] + 1

            # Validation: all the data of an entity is unique
            if (dat.cod_entity_target, dat.column_name_target, dat.num_branch, dat.satellite_name, dat.num_connection) not in row_by_pk:
                row_by_pk.append((dat.cod_entity_target, dat.column_name_target, dat.num_branch, dat.satellite_name, dat.num_connection))
            else:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ '+dat.cod_entity_target+' ] have some columns with same name', LOG_LEVEL_ERROR)

            # Validation: Ordinal Position for different branches and same column need to be the same
            if(dat.cod_entity_target, dat.column_name_target) not in all_ordinal_position_same_col_same_pos:
                all_ordinal_position_same_col_same_pos[dat.cod_entity_target, dat.column_name_target] = dat.ordinal_position
            else:
                if dat.ordinal_position != all_ordinal_position_same_col_same_pos[dat.cod_entity_target, dat.column_name_target]:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ ' + dat.cod_entity_target + ' ] ordinal position needs to be the same if two columns are named equal', LOG_LEVEL_ERROR)

            # Validation: Ordinal Position for different branches and same column need to be the same
            if (dat.cod_entity_target, dat.ordinal_position) not in all_ordinal_position_dif_pos:
                all_ordinal_position_dif_pos[dat.cod_entity_target, dat.ordinal_position] = dat.column_name_target
            else:
                if dat.column_name_target != all_ordinal_position_dif_pos[dat.cod_entity_target, dat.ordinal_position]:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [ ' + dat.cod_entity_target + ' ] ordinal position needs to be diferent for all the columns', LOG_LEVEL_ERROR)


        #Validation: all the sources have the same origin type
        for x in all_sources_origin_type.items():
            if (x[1]['incremental'] > 0 and x[1]['total'] > 0) or (x[1]['incremental'] > 0 and x[1]['cdc'] > 0) or (x[1]['cdc'] > 0 and x[1]['total'] > 0):
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> a source [ '+ x[0] +' ]can not have diferent origin types', LOG_LEVEL_ERROR)

        # Validation: all the branches are consecutive
        for x in all_entities_by_branch.items():
            start_branch = 1
            for y in x[1].items():
                if start_branch != y[0]:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> Num branches form entity [' + x[0] + '] are not consecutive from 0', LOG_LEVEL_ERROR)
                start_branch += 1

        last_bk = -1
        last_rs = -1
        last_tn = -1
        last_seq = -1
        last_ad = -1
        last_dk = -1
        last_num_connection = -1

        # Validation: all the branches has the same number of elements (same BKs, ADs, Tns...) and not repeated
        for x in all_entities_by_branch.items():
            first_element = True
            for y in x[1].items():
                if y[1]['seq']>1:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] Only 1 SEQ data type is permitted' + x[0], LOG_LEVEL_ERROR)
                if y[1]['ad']>1:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] Only 1 AD data type is permitted' + x[0], LOG_LEVEL_ERROR)
                if y[1]['rs']>1:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] Only 1 RS data type is permitted' + x[0], LOG_LEVEL_ERROR)
                if first_element:
                    last_bk = y[1]['bk']
                    last_rs = y[1]['rs']
                    last_tn = y[1]['tn']
                    last_seq = y[1]['seq']
                    last_ad = y[1]['ad']
                    last_dk = y[1]['dk']
                    last_num_connection = y[1]['num_connection']
                    first_element = False
                if last_bk != y[1]['bk'] or last_rs != y[1]['rs'] or last_tn != y[1]['tn'] or last_seq != y[1]['seq'] or last_ad != y[1]['ad'] or last_num_connection != y[1]['num_connection'] or last_dk != y[1]['dk']:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> different number of elements by entity on ' + x[0], LOG_LEVEL_ERROR)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_entry_datavault(self):
        table_validation = 'DATAVAULT'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True
        for dat in self.metadata.entry_dv_entity:
            # Validation: EFFECTIVITY SAT is recommended to be total and can only be indicated on LINK
            if dat.name_effectivity_satellite is not None and dat.name_effectivity_satellite != '':
                if dat.entity_type != ENTITY_LINK:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [' + dat.name_effectivity_satellite + '] can only be setted on LINK', LOG_LEVEL_ERROR)
                has_warned = False
                for x in self.metadata.entry_dv_mappings:
                    if x.cod_entity_target == dat.cod_entity:
                        if x.origin_is_total == 0 and not has_warned:
                            has_warned = True
                            self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] ' + x.cod_entity_target + ' has an Effectivity Satellite and the origin is not total', LOG_LEVEL_WARNING)
            # Validation: RECORD TRACKING SAT must have an Applied Date
            if dat.name_record_tracking_satellite is not None and dat.name_record_tracking_satellite != '':
                has_ad = False
                for x in self.metadata.entry_dv_mappings:
                    if x.cod_entity_target == dat.cod_entity:
                        if x.key_type == KEY_TYPE_APPLIED_DATE:
                            has_ad = True
                if not has_ad:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [' + dat.name_record_tracking_satellite+'] must have an Applied Date attribute', LOG_LEVEL_ERROR)
            # Validation: EFFECTIVITY SAT must have a DK.
            if dat.name_effectivity_satellite is not None and dat.name_effectivity_satellite != '':
                has_dk = False
                for x in self.metadata.entry_dv_mappings:
                    if x.cod_entity_target == dat.cod_entity:
                        if x.key_type == KEY_TYPE_DRIVENKEY:
                            has_dk = True
                if not has_dk:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> [' + dat.name_effectivity_satellite + '] must have a Driven Key', LOG_LEVEL_ERROR)

        self.log.log(self.validator_name, 'Finish metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result