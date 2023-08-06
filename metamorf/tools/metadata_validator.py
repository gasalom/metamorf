from metamorf.constants import *
from metamorf.tools.log import Log

class MetadataValidator:

    def __init__(self, metadata, source_connection, configuration_file, log):
        self.metadata = metadata
        self.log = log
        self.validator_name = 'Metadata Validator'
        self.configuration_file = configuration_file
        self.connection = source_connection

        self.initialize_references()
        '''
        COMO OBTENER las columnas de una tabla
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

    def validate_metadata(self):
        self.log.log(self.validator_name, 'Starting Metadata Entry Validation', LOG_LEVEL_INFO)
        result = self.validate_metadata_entry_path()
        result = result and self.validate_metadata_entry_entity()
        result = result and self.validate_metadata_entry_dataset_mappings()




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
            if entity.cod_entity not in self.all_cod_entity_elt: self.all_cod_entity_elt.append(entity.cod_entity)

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
            if entry.key_type not in self.all_key_type and entry.key_type is not None and entry.key_type != '':
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
            #TODO: verificar que todos los num branch tienen el mismo numero de registros

            if entry.sw_distinct not in [0,1]:
                result = False
                self.log.log(self.validator_name, 'Metadata Entry [ '+ table_validation + ' ] -> [ SW_DISTINCT ] only accepts 0/1 values', LOG_LEVEL_ERROR)

            if entry.cod_entity_target in all_entities_by_branch:
                if entry.num_branch in all_entities_by_branch[entry.cod_entity_target]:
                    all_entities_by_branch[entry.cod_entity_target][entry.num_branch] = all_entities_by_branch[entry.cod_entity_target][entry.num_branch] +1
                else:
                    all_entities_by_branch[entry.cod_entity_target][entry.num_branch] = 1
            else:
                all_entities_by_branch[entry.cod_entity_target] = dict()
                all_entities_by_branch[entry.cod_entity_target][entry.num_branch] = 1

        #TODO: renombrar y poner bonito
        for x in all_entities_by_branch.items():
            num_records_by_branch = 0
            for y in x[1].items():
                if num_records_by_branch != y[1] and num_records_by_branch != 0:
                    result = False
                    self.log.log(self.validator_name, 'Metadata Entry [ ' + table_validation + ' ] -> Num branches not equal', LOG_LEVEL_ERROR)
                num_records_by_branch = y[1]



        self.log.log(self.validator_name, 'Finished metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result

    def validate_metadata_x(self):
        table_validation = 'ENTRY_PATH'
        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        result = True

        for path in self.metadata.X:
            pass

        self.log.log(self.validator_name, 'Start metadata validation on [ ' + table_validation + ' ]', LOG_LEVEL_DEBUG)
        return result


