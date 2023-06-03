from metamorf.tools.database_objects import *
from metamorf.constants import *
from metamorf.tools.log import Log
import re

class Metadata:

    def __init__(self, log: Log):
        self.log = log
        # Entry Tables
        self.entry_order = []
        self.entry_aggregators = []
        self.entry_filters = []
        self.entry_dataset_relationship = []
        self.entry_entity = []
        self.entry_having = []
        self.entry_path = []
        self.entry_dataset_mappings = []
        self.entry_dv_entity = []
        self.entry_dv_mappings = []
        self.entry_dv_properties = []
        self.entry_files = []
        # Metamorf Tables
        self.om_dataset = []
        self.om_dataset_dv = []
        self.om_dataset_execution = []
        self.om_dataset_t_order = []
        self.om_dataset_t_agg = []
        self.om_dataset_t_distinct = []
        self.om_dataset_specification = []
        self.om_dataset_relationships = []
        self.om_dataset_t_filter = []
        self.om_dataset_t_mapping = []
        self.om_dataset_path = []
        self.om_dataset_t_having = []
        self.om_properties = []
        self.om_dataset_hardcoded = []
        self.om_dataset_file = []
        # Reference Tables
        self.om_ref_query_type = []
        self.om_ref_order_type = []
        self.om_ref_join_type = []
        self.om_ref_modules = []
        self.om_ref_entity_type = []
        self.om_ref_key_type = []
        # IM Tables
        self.om_dataset_information = []
        self.om_relationships = []
        self.om_dataset_specification_information = []


    def add_entry_order(self, entry_order_list: list):
        for entry_order in entry_order_list:
            try:
                self.entry_order.append(EntryOrder(entry_order[0], entry_order[1], entry_order[2], entry_order[3], entry_order[4], entry_order[5]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry Order]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True


    def add_entry_aggregators(self, entry_aggregators_list: list):
        for entry_aggregators in entry_aggregators_list:
            try:
                self.entry_aggregators.append(EntryAggregators(entry_aggregators[0], entry_aggregators[1],entry_aggregators[2], entry_aggregators[3], entry_aggregators[4]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry Aggregators]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_entry_filters(self, entry_filters_list: list):
        for entry_filters in entry_filters_list:
            try:
                self.entry_filters.append(EntryFilters(entry_filters[0], entry_filters[1], entry_filters[2], entry_filters[3]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry Filters]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_entry_files(self, entry_files_list: list):
        for entry_files in entry_files_list:
            try:
                self.entry_files.append(EntryFiles(entry_files[0], entry_files[1], entry_files[2], entry_files[3], entry_files[4]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry Files]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_entry_having(self, entry_having_list: list):
        for entry_having in entry_having_list:
            try:
                self.entry_having.append(EntryHaving(entry_having[0], entry_having[1], entry_having[2], entry_having[3]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry Having]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_entry_dataset_relationship(self, entry_dataset_relationship_list: list):
        for entry_dataset_relationship in entry_dataset_relationship_list:
            try:
                self.entry_dataset_relationship.append(EntryDatasetRelationships(entry_dataset_relationship[0], entry_dataset_relationship[1], entry_dataset_relationship[2], entry_dataset_relationship[3], entry_dataset_relationship[4], entry_dataset_relationship[5]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry Relationship]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_entry_entity(self, entry_entity_list: list):
        for entry_entity in entry_entity_list:
            try:
                self.entry_entity.append(EntryEntity(entry_entity[0], entry_entity[1], entry_entity[2], entry_entity[3], entry_entity[4], entry_entity[5]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry Entity]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_entry_path(self, entry_path_list: list):
        for entry_path in entry_path_list:
            try:
                self.entry_path.append(EntryPath(entry_path[0], entry_path[1], entry_path[2], entry_path[3]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry Order]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_entry_dataset_mappings(self, entry_dataset_mappings_list: list):
        for entry_dataset_mappings in entry_dataset_mappings_list:
            try:
                self.entry_dataset_mappings.append(EntryDatasetMappings(entry_dataset_mappings[0], entry_dataset_mappings[1], entry_dataset_mappings[2], entry_dataset_mappings[3], entry_dataset_mappings[4], entry_dataset_mappings[5], entry_dataset_mappings[6], entry_dataset_mappings[7], entry_dataset_mappings[8], entry_dataset_mappings[9], entry_dataset_mappings[10], entry_dataset_mappings[11]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry Order]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_entry_dv_entity(self, entry_dv_entity_list: list):
        for entry_dv_entity in entry_dv_entity_list:
            try:
                self.entry_dv_entity.append(EntryDvEntry(entry_dv_entity[0],entry_dv_entity[1],entry_dv_entity[2],entry_dv_entity[3],entry_dv_entity[4],entry_dv_entity[5],entry_dv_entity[6],entry_dv_entity[7]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry DV Entity]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_entry_dv_mappings(self, entry_dv_mappings_list: list):
        for entry_dv_mappings in entry_dv_mappings_list:
            try:
                self.entry_dv_mappings.append(EntryDvMappings(entry_dv_mappings[0],entry_dv_mappings[1],entry_dv_mappings[2],entry_dv_mappings[3],entry_dv_mappings[4],entry_dv_mappings[5],entry_dv_mappings[6],entry_dv_mappings[7],entry_dv_mappings[8],entry_dv_mappings[9],entry_dv_mappings[10],entry_dv_mappings[11],entry_dv_mappings[12],entry_dv_mappings[13],entry_dv_mappings[14],entry_dv_mappings[15]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry DV Mappings]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_entry_dv_properties(self, entry_dv_properties_list: list):
        for entry_dv_properties in entry_dv_properties_list:
            try:
                self.entry_dv_properties.append(EntryDvProperties(entry_dv_properties[0],entry_dv_properties[1],entry_dv_properties[2],entry_dv_properties[3]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Entry DV Mappings]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset(self, om_dataset_list: list):
        for om_dataset in om_dataset_list:
            try:
                self.om_dataset.append(OmDataset(om_dataset[0],om_dataset[1],om_dataset[2],om_dataset[3],om_dataset[4],om_dataset[5],om_dataset[6]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_dv(self, om_dataset_dv_list: list):
        for om_dataset_dv in om_dataset_dv_list:
            try:
                self.om_dataset_dv.append(OmDatasetDv(om_dataset_dv[0],om_dataset_dv[1],om_dataset_dv[2],om_dataset_dv[3],om_dataset_dv[4]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset DV]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_execution(self, om_dataset_execution_list: list):
        for om_dataset_execution in om_dataset_execution_list:
            try:
                self.om_dataset_execution.append(OmDatasetExecution(om_dataset_execution[0],om_dataset_execution[1],om_dataset_execution[2],om_dataset_execution[3],om_dataset_execution[4]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Execution]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_t_order(self, om_dataset_t_order_list: list):
        for om_dataset_t_order in om_dataset_t_order_list:
            try:
                self.om_dataset_t_order.append(OmDatasetTOrder(om_dataset_t_order[0],om_dataset_t_order[1],om_dataset_t_order[2],om_dataset_t_order[3],om_dataset_t_order[4],om_dataset_t_order[5],om_dataset_t_order[6],om_dataset_t_order[7]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Order]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_t_agg(self, om_dataset_t_agg_list: list):
        for om_dataset_t_agg in om_dataset_t_agg_list:
            try:
                self.om_dataset_t_agg.append(OmDatasetTAgg(om_dataset_t_agg[0],om_dataset_t_agg[1],om_dataset_t_agg[2],om_dataset_t_agg[3],om_dataset_t_agg[4],om_dataset_t_agg[5],om_dataset_t_agg[6]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Aggregator]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_t_distinct(self, om_dataset_t_distinct_list: list):
        for om_dataset_t_distinct in om_dataset_t_distinct_list:
            try:
                self.om_dataset_t_distinct.append(OmDatasetTDistinct(om_dataset_t_distinct[0],om_dataset_t_distinct[1],om_dataset_t_distinct[2],om_dataset_t_distinct[3],om_dataset_t_distinct[4],om_dataset_t_distinct[5],om_dataset_t_distinct[6]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Distinct]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_specification(self, om_dataset_specification_list: list):
        for om_dataset_specification in om_dataset_specification_list:
            try:
                self.om_dataset_specification.append(OmDatasetSpecification(om_dataset_specification[0],om_dataset_specification[1],om_dataset_specification[2],om_dataset_specification[3],om_dataset_specification[4],om_dataset_specification[5],om_dataset_specification[6],om_dataset_specification[7],om_dataset_specification[8],om_dataset_specification[9],om_dataset_specification[10],om_dataset_specification[11],om_dataset_specification[12]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Specification]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_relationships(self, om_dataset_relationships_list: list):
        for om_dataset_relationships in om_dataset_relationships_list:
            try:
                self.om_dataset_relationships.append(OmDatasetRelationships(om_dataset_relationships[0],om_dataset_relationships[1],om_dataset_relationships[2],om_dataset_relationships[3],om_dataset_relationships[4],om_dataset_relationships[5],om_dataset_relationships[6]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Relationships]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_t_filter(self, om_dataset_t_filter_list: list):
        for om_dataset_t_filter in om_dataset_t_filter_list:
            try:
                self.om_dataset_t_filter.append(OmDatasetTFilter(om_dataset_t_filter[0],om_dataset_t_filter[1],om_dataset_t_filter[2],om_dataset_t_filter[3],om_dataset_t_filter[4],om_dataset_t_filter[5],om_dataset_t_filter[6]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Filter]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_t_mapping(self, om_dataset_t_mapping_list: list):
        for om_dataset_t_mapping in om_dataset_t_mapping_list:
            try:
                self.om_dataset_t_mapping.append(OmDatasetTMapping(om_dataset_t_mapping[0],om_dataset_t_mapping[1],om_dataset_t_mapping[2],om_dataset_t_mapping[3],om_dataset_t_mapping[4],om_dataset_t_mapping[5],om_dataset_t_mapping[6]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Mapping]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_path(self, om_dataset_path_list: list):
        for om_dataset_path in om_dataset_path_list:
            try:
                self.om_dataset_path.append(OmDatasetPath(om_dataset_path[0],om_dataset_path[1],om_dataset_path[2],om_dataset_path[3],om_dataset_path[4],om_dataset_path[5]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Path]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_t_having(self, om_dataset_t_having_list: list):
        for om_dataset_t_having in om_dataset_t_having_list:
            try:
                self.om_dataset_t_having.append(OmDatasetTHaving(om_dataset_t_having[0],om_dataset_t_having[1],om_dataset_t_having[2],om_dataset_t_having[3],om_dataset_t_having[4],om_dataset_t_having[5],om_dataset_t_having[6]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Having]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_properties(self, om_properties_list: list):
        for om_properties in om_properties_list:
            try:
                self.om_properties.append(OmProperties(om_properties[0],om_properties[1],om_properties[2]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Properties]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_hardcoded(self, om_dataset_hardcoded_list: list):
        for om_dataset_hardcoded in om_dataset_hardcoded_list:
            try:
                self.om_dataset_hardcoded.append(OmDatasetHardcoded(om_dataset_hardcoded[0],om_dataset_hardcoded[1],om_dataset_hardcoded[2],om_dataset_hardcoded[3],om_dataset_hardcoded[4],om_dataset_hardcoded[5],om_dataset_hardcoded[6]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Hardcoded]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_ref_modules(self, om_ref_modules_list: list):
        for om_ref_modules in om_ref_modules_list:
            try:
                self.om_ref_modules.append(OmRefModules(om_ref_modules[0],om_ref_modules[1],om_ref_modules[2],om_ref_modules[3]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Reference Modules]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_ref_query_type(self, om_ref_query_type_list: list):
        for om_ref_query_type in om_ref_query_type_list:
            try:
                self.om_ref_query_type.append(OmRefQueryType(om_ref_query_type[0],om_ref_query_type[1],om_ref_query_type[2]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Reference Query Type]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_ref_order_type(self, om_ref_order_type_list: list):
        for om_ref_order_type in om_ref_order_type_list:
            try:
                self.om_ref_order_type.append(OmRefOrderType(om_ref_order_type[0],om_ref_order_type[1],om_ref_order_type[2],om_ref_order_type[3]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Reference Order Type]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_ref_join_type(self, om_ref_join_type_list: list):
        for om_ref_join_type in om_ref_join_type_list:
            try:
                self.om_ref_join_type.append(OmRefJoinType(om_ref_join_type[0],om_ref_join_type[1],om_ref_join_type[2],om_ref_join_type[3]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Reference Join Type]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_ref_entity_type(self, om_ref_entity_type_list: list):
        for om_ref_entity_type in om_ref_entity_type_list:
            try:
                self.om_ref_entity_type.append(OmRefEntityType(om_ref_entity_type[0],om_ref_entity_type[1],om_ref_entity_type[2],om_ref_entity_type[3],om_ref_entity_type[4]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Reference Entity Type]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_ref_key_type(self, om_ref_key_type_list: list):
        for om_ref_key_type in om_ref_key_type_list:
            try:
                self.om_ref_key_type.append(OmRefKeyType(om_ref_key_type[0],om_ref_key_type[1],om_ref_key_type[2]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Reference Key Type]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_information(self, om_dataset_information_list):
        for om_dataset_information in om_dataset_information_list:
            try:
                self.om_dataset_information.append(OmDatasetInformation(om_dataset_information[0],om_dataset_information[1],om_dataset_information[2],om_dataset_information[3],om_dataset_information[4],om_dataset_information[5],om_dataset_information[6],om_dataset_information[7],om_dataset_information[8],om_dataset_information[9],om_dataset_information[10],om_dataset_information[11]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Information]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_relationships(self, om_relationships_list):
        for om_relationships in om_relationships_list:
            try:
                self.om_relationships.append(OmRelationships(om_relationships[0],om_relationships[1],om_relationships[2],om_relationships[3],om_relationships[4],om_relationships[5],om_relationships[6],om_relationships[7],om_relationships[8],om_relationships[9]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Relationships]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_file(self, om_dataset_file_list):
        for om_dataset_file in om_dataset_file_list:
            try:
                self.om_dataset_file.append(OmDatasetFile(om_dataset_file[0],om_dataset_file[1],om_dataset_file[2],om_dataset_file[3],om_dataset_file[4],om_dataset_file[5],om_dataset_file[6]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset File]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def add_om_dataset_specification_information(self, om_dataset_specification_information_list):
        for om_dataset_specification_information in om_dataset_specification_information_list:
            try:
                self.om_dataset_specification_information.append(OmDatasetSpecificationInformation(om_dataset_specification_information[0],om_dataset_specification_information[1],om_dataset_specification_information[2],om_dataset_specification_information[3],om_dataset_specification_information[4],om_dataset_specification_information[5],om_dataset_specification_information[6],om_dataset_specification_information[7],om_dataset_specification_information[8]))
            except Exception as e:
                self.log.log("Metadata Loader", "Error loading [Dataset Specification Information]: " + str(e), LOG_LEVEL_ERROR)
                return False
        return True

    def get_dataset_from_dataset_name(self, dataset):
        """Return ID_DATASET from DATASET_NAME. If not exists returns None"""
        for d in self.om_dataset:
            if d.dataset_name == dataset and (d.end_date is None or d.end_date == 'NULL'): return d
        return None

    def get_entry_entity_from_cod_entity(self, cod_entity):
        for d in self.entry_entity:
            if d.cod_entity == cod_entity: return d
        return None

    def get_num_branches_on_entry_dv_from_cod_entity_name(self, cod_entity_name):
        num_branches = 0
        for d in self.entry_dv_mappings:
            if d.cod_entity_target != cod_entity_name: continue
            if d.num_branch > num_branches: num_branches = d.num_branch
        return num_branches

    def get_num_connections_on_entry_dv_from_cod_entity_name(self, cod_entity_name):
        num_connection = 0
        for d in self.entry_dv_mappings:
            if d.cod_entity_target != cod_entity_name: continue
            if d.num_connection > num_connection: num_connection = d.num_connection
        return num_connection

    def get_all_bk_from_entry_dv_cod_entity_target_and_num_branch(self, cod_entity, num_branch):
        all_bk = []
        for d in self.entry_dv_mappings:
            if d.cod_entity_target != cod_entity or d.num_branch != num_branch: continue
            if d.key_type.upper() == KEY_TYPE_BUSINESS_KEY or d.key_type.upper() == KEY_TYPE_DRIVENKEY: all_bk.append(d)
        return all_bk

    def get_all_bk_from_entry_dv_cod_entity_target_and_num_branch_and_num_connection(self, cod_entity, num_branch, num_connection):
        all_bk = []
        for d in self.entry_dv_mappings:
            if d.cod_entity_target != cod_entity or d.num_branch != num_branch or d.num_connection != num_connection: continue
            if d.key_type.upper() == KEY_TYPE_BUSINESS_KEY or d.key_type.upper() == KEY_TYPE_DRIVENKEY:all_bk.append(d)
        return all_bk


    def get_dataset_execution_from_id_dataset(self, id_dataset):
        for execution in self.om_dataset_execution:
            if execution.id_dataset == id_dataset and (execution.end_date is None or execution.end_date == 'NULL'): return execution
        return None

    def get_dataset_dv_from_id_dataset(self, id_dataset):
        for dataset_dv in self.om_dataset_dv:
            if dataset_dv.id_dataset == id_dataset and (dataset_dv.end_date is None or dataset_dv.end_date == 'NULL'): return dataset_dv
        return None

    def get_path_from_database_and_schema(self, database, schema):
        """Return PATH from DATABASE and SCHEMA names. If not exists returns None"""
        for path in self.om_dataset_path:
            if str(path.database_name) == str(database) and str(path.schema_name) == str(schema) and (path.end_date is None or path.end_date == 'NULL'): return path
        return None

    def get_path_from_id_path(self, id_path):
        """Return PATH from ID_PATH. If not exists returns None"""
        for path in self.om_dataset_path:
            if path.id_path == id_path and (path.end_date is None or path.end_date == 'NULL'): return path
        return None

    def get_path_from_dataset_name(self, dataset_name):
        for dataset in self.om_dataset:
            if dataset.dataset_name == dataset_name and (dataset.end_date is None or dataset.end_date == 'NULL'):
                for path in self.om_dataset_path:
                    if path.id_path == dataset.id_path: return path
        return None

    def get_entry_path_from_cod_path(self, cod_path):
        for entry_path in self.entry_path:
            if entry_path.cod_path == cod_path: return entry_path
        return None

    def get_entity_type_from_entity_type_name(self, entity_type_name):
        for entity_type in self.om_ref_entity_type:
            if entity_type.entity_type_name == entity_type_name: return entity_type
        return None

    def get_key_type_from_key_type_name(self, key_type_name):
        for key_type in self.om_ref_key_type:
            if key_type.key_type_name == key_type_name: return key_type
        return None

    def get_cols_from_cod_entity_on_entry(self,cod_entity):
        all_cols = []
        columns_name_added = []
        for col in self.entry_dataset_mappings:
            if col.cod_entity_target == cod_entity:
                if col.key_type is None: col.key_type = "NULL"
                columna = Column(col.ordinal_position, col.column_name_target, col.column_type_target, None, col.key_type, 0,col.column_length,col.column_precision,0)
                if col.column_name_target not in columns_name_added:
                    all_cols.append(columna)
                    columns_name_added.append(col.column_name_target)
        return all_cols

    def get_order_from_id_dataset_and_id_dataset_spec_and_id_branch(self, id_dataset, id_dataset_spec, id_branch):
        for order in self.om_dataset_t_order:
            if order.id_dataset == id_dataset and order.id_dataset_spec == id_dataset_spec and order.id_branch == id_branch and (order.end_date is None or order.end_date == 'NULL'): return order
        return None

    def get_aggregator_from_id_dataset_and_id_dataset_spec_and_id_branch(self, id_dataset, id_dataset_spec, id_branch):
        for agg in self.om_dataset_t_agg:
            if agg.id_dataset == id_dataset and agg.id_dataset_spec and id_dataset_spec and agg.id_branch == id_branch and (agg.end_date is None or agg.end_date == 'NULL'): return agg
        return None

    def get_relationship_from_id_dataset_spec_master_and_detail(self, id_dataset_spec_master, id_dataset_spec_detail):
        for relationship in self.om_dataset_relationships:
            if relationship.id_dataset_spec_master == id_dataset_spec_master and relationship.id_dataset_spec_detail == id_dataset_spec_detail and (relationship.end_date is None or relationship.end_date == 'NULL'): return relationship
        return None

    def get_distinct_from_id_dataset_and_branch(self, id_dataset, id_branch):
        for distinct in self.om_dataset_t_distinct:
            if distinct.id_dataset == id_dataset and id_branch == distinct.id_branch and (distinct.end_date is None or distinct.end_date == 'NULL'): return distinct
        return None

    def get_dataset_t_mapping_from_id_branch_and_id_dataset_spec_and_value_mapping(self, id_branch, id_dataset_spec, value_mapping):
        for mapping in self.om_dataset_t_mapping:
            if mapping.id_branch == id_branch and mapping.id_dataset_spec == id_dataset_spec and mapping.value_mapping == value_mapping and mapping.end_date is None: return mapping
        return None

    def get_dataset_t_mapping_from_id_branch_and_id_dataset_spec(self, id_branch, id_dataset_spec):
        for mapping in self.om_dataset_t_mapping:
            if mapping.id_branch == id_branch and mapping.id_dataset_spec == id_dataset_spec and mapping.end_date is None: return mapping
        return None

    def get_dataset_t_mapping_from_id_dataset_spec(self, id_dataset_spec):
        dataset_t_mapping = []
        for mapping in self.om_dataset_t_mapping:
            if int(mapping.id_dataset_spec) == int(id_dataset_spec) and (mapping.end_date is None or mapping.end_date == 'NULL'):
                dataset_t_mapping.append(mapping)
        return dataset_t_mapping

    def get_dataset_t_filter_from_id_dataset_and_id_branch_and_value_filter(self, id_dataset, id_branch, value_filter):
        for filter in self.om_dataset_t_filter:
            if filter.id_dataset == id_dataset and filter.id_branch == id_branch and filter.value_filter == value_filter and (filter.end_date is None or filter.end_date == 'NULL'): return filter
        return None

    def get_dataset_t_having_from_id_dataset_and_id_branch_and_value_having(self, id_dataset, id_branch, value_having):
        for having in self.om_dataset_t_having:
            if int(having.id_dataset) == int(id_dataset) and int(having.id_branch) == int(id_branch) and having.value_having == value_having and (having.end_date is None or having.end_date == 'NULL'): return having
        return None

    def get_table_name_from_cod_entity_on_entry(self, cod_entity):
        for entity in self.entry_entity:
            if entity.cod_entity == cod_entity: return entity.table_name
        return None

    def get_dataset_spec_from_id_dataset_and_column_name(self, id_dataset, column_name):
        for dataset_spec in self.om_dataset_specification:
            if dataset_spec.id_dataset == id_dataset and dataset_spec.column_name == column_name and (dataset_spec.end_date is None or dataset_spec.end_date == 'NULL'): return dataset_spec
        return None

    def get_order_type_from_order_type_value(self, order_type_value):
        for order_type in self.om_ref_order_type:
            if order_type.order_type_value.upper() == order_type_value.upper(): return order_type
        return None

    def get_order_type_from_id_order_type(self, id_order_type):
        for order_type in self.om_ref_order_type:
            if order_type.id_order_type == id_order_type: return order_type
        return None

    def get_join_type_from_join_name(self, join_name):
        for join_type in self.om_ref_join_type:
            if join_type.join_name.upper() == join_name.upper(): return join_type
        return None

    def get_all_columns_from_table_name(self, table_name):
        all_columns = []
        id_dataset = self.get_id_dataset_from_table_name(table_name)
        for col in self.om_dataset_specification:
            if col.id_dataset == id_dataset and (col.end_date is None or col.end_date=='NULL'): all_columns.append(col.column_name)
        return all_columns

    def get_id_dataset_from_table_name(self, table_name):
        for dataset in self.om_dataset:
            if dataset.dataset_name == table_name and (dataset.end_date is None or dataset.end_date=='NULL') : return dataset.id_dataset
        return None

    def get_dataset_from_id_dataset(self, id_dataset):
        for dataset in self.om_dataset:
            if dataset.id_dataset == id_dataset: return dataset
        return None

    def get_dataset_spec_from_id_dataset_spec(self, id_dataset_spec):
        for dataset_spec in self.om_dataset_specification:
            if dataset_spec.id_dataset_spec == id_dataset_spec:
                return dataset_spec
        return None

    def get_all_source_tables_from_target_table_name(self, target_table_name):
        all_source_tables = []
        dataset = self.get_dataset_from_dataset_name(target_table_name)
        for dataset_spec in self.om_dataset_specification:
            if dataset_spec.id_dataset == dataset.id_dataset:
                id_dataset_spec = dataset_spec.id_dataset_spec
                for map in [x for x in self.om_dataset_t_mapping if (x.end_date is None or x.end_date == "NULL") and x.id_dataset_spec == id_dataset_spec]:
                    column_origins = re.findall(r'\[(\d+)\]', map.value_mapping)
                    for col in column_origins:
                        dataset_spec_origin = self.get_dataset_spec_from_id_dataset_spec(int(col))
                        dataset_origin = self.get_dataset_from_id_dataset(dataset_spec_origin.id_dataset)
                        if dataset_origin.dataset_name not in all_source_tables and dataset_origin.dataset_name != target_table_name:
                            all_source_tables.append(dataset_origin.dataset_name)
        all_source_tables = list(dict.fromkeys(all_source_tables))
        return all_source_tables

    def get_all_source_tables_from_target_table_name_and_branch(self, target_table_name, num_branch):
        all_source_tables = []
        dataset = self.get_dataset_from_dataset_name(target_table_name)
        for dataset_spec in self.om_dataset_specification:
            if dataset_spec.id_dataset == dataset.id_dataset:
                id_dataset_spec = dataset_spec.id_dataset_spec
                for map in [x for x in self.om_dataset_t_mapping if (x.end_date is None or x.end_date == "NULL") and x.id_dataset_spec == id_dataset_spec and x.id_branch == num_branch]:
                    column_origins = re.findall(r'\[(\d+)\]', map.value_mapping)
                    for col in column_origins:
                        dataset_spec_origin = self.get_dataset_spec_from_id_dataset_spec(int(col))
                        dataset_origin = self.get_dataset_from_id_dataset(dataset_spec_origin.id_dataset)
                        if dataset_origin.id_entity_type != self.get_entity_type_from_entity_type_name(ENTITY_WITH).id_entity_type:
                            path = self.get_path_from_dataset_name(dataset_origin.dataset_name)
                            path_fqdn = self.get_fqdn_from_path(path)
                            if path_fqdn != "": path_fqdn += "."
                            new_dataset = path_fqdn + dataset_origin.dataset_name
                        else:
                            new_dataset = dataset_origin.dataset_name
                        if new_dataset not in all_source_tables:
                            all_source_tables.append(new_dataset)
        return all_source_tables


    def get_fqdn_from_path(self, path):
        fqdn = ""
        if path.database_name is None or path.database_name == "":
            if path.schema_name is not None and path.schema_name != "":
                fqdn = path.schema_name
        else:
            if path.schema_name is None or path.schema_name == "":
                fqdn = path.database_name
            else:
                fqdn = path.database_name + "." + path.schema_name
        return fqdn

    def get_num_branches_from_dataset_name(self, dataset_name):
        dataset = self.get_dataset_from_dataset_name(dataset_name)
        max_num_branch = 0
        for dataset_spec in [x for x in self.om_dataset_specification if x.end_date is None]:
            if dataset_spec.id_dataset == dataset.id_dataset:
                for map in [x for x in self.om_dataset_t_mapping if (x.end_date is None or x.end_date == '') and x.id_dataset_spec == dataset_spec.id_dataset_spec]:
                    if map.id_branch>max_num_branch: max_num_branch=map.id_branch
        return max_num_branch

    def get_list_id_dataset_spec_from_dataset_name(self, dataset_name):
        dataset = self.get_dataset_from_dataset_name(dataset_name)
        list_id_dataset_spec = []
        for dataset_spec in [x for x in self.om_dataset_specification if x.end_date is None]:
            if dataset_spec.id_dataset == dataset.id_dataset:
                list_id_dataset_spec.append(dataset_spec.id_dataset_spec)
        return list_id_dataset_spec

    def get_tables_dot_column_from_id_dataset_spec(self, id_dataset_spec):
        dataset_spec = self.get_dataset_spec_from_id_dataset_spec(int(id_dataset_spec))
        dataset = self.get_dataset_from_id_dataset(dataset_spec.id_dataset)
        return dataset.dataset_name +"."+dataset_spec.column_name

    def get_query_type_from_query_type_name(self, query_type_name):
        for query in self.om_ref_query_type:
            if query.query_type_name == query_type_name: return query
        return None

    def get_version_from_metadata_database(self):
        for property in self.om_properties:
            if property.property.upper() == 'VERSION': return property.value
        raise ValueError("Metadata Database Version unstable")

    def get_dataset_fqdn_from_dataset_name(self, dataset_name):
        path = self.get_path_from_dataset_name(dataset_name)
        fqdn = self.get_fqdn_from_path(path)
        if fqdn != "": fqdn += "."
        return fqdn + dataset_name

    def get_record_source_on_dv_from_cod_entity_target_and_num_branch(self, cod_entity_target, num_branch):
        for d in self.entry_dv_mappings:
            if d.key_type != KEY_TYPE_RECORD_SOURCE: continue
            if d.cod_entity_target == cod_entity_target and d.num_branch == num_branch:
                return d
        return None

    def get_applied_date_on_dv_from_cod_entity_target(self, cod_entity_target, num_branch):
        for d in self.entry_dv_mappings:
            if d.key_type != KEY_TYPE_APPLIED_DATE: continue
            if d.cod_entity_target == cod_entity_target and d.num_branch == num_branch:
                return d
        return None

    def get_dependent_child_key_on_dv_from_satellite_name(self, satellite_name):
        all_dck = []
        for d in self.entry_dv_mappings:
            if d.key_type != KEY_TYPE_DEPENDENT_CHILD_KEY: continue
            if d.satellite_name == satellite_name: all_dck.append(d)
        return all_dck

    def get_tenant_on_dv_from_cod_entity_target_and_num_branch(self, cod_entity_target, num_branch):
        all_tenant = []
        for d in self.entry_dv_mappings:
            if d.key_type != KEY_TYPE_TENANT: continue
            if d.cod_entity_target == cod_entity_target and d.num_branch == num_branch:
                all_tenant.append(d)
        return all_tenant

    def get_seq_on_dv_from_cod_entity_target_and_num_branch(self, cod_entity_target, num_branch):
        all_seq = []
        for d in self.entry_dv_mappings:
            if d.key_type != KEY_TYPE_SEQUENCE: continue
            if d.cod_entity_target == cod_entity_target and d.num_branch == num_branch:
                all_seq.append(d)
        return all_seq

    def get_tenant_on_dv_from_cod_entity_target_and_num_branch_and_num_connection(self, cod_entity_target, num_branch, num_connection):
        all_tenant = []
        for d in self.entry_dv_mappings:
            if d.key_type != KEY_TYPE_TENANT: continue
            if d.cod_entity_target == cod_entity_target and d.num_branch == num_branch and d.num_connection == num_connection:
                all_tenant.append(d)
        return all_tenant

    def get_attributes_on_dv_from_satellite_name(self, satellite_name):
        all_attributes = []
        for d in self.entry_dv_mappings:
            if d.key_type != KEY_TYPE_ATTRIBUTE and d.key_type != KEY_TYPE_STATUS: continue
            if d.satellite_name == satellite_name: all_attributes.append(d)
        return all_attributes

    def get_all_satellites_info_from_hub(self, cod_entity_target):
        all_satellites = []
        for d in self.entry_dv_mappings:
            if d.cod_entity_target == cod_entity_target:
                if d.satellite_name != '' and d.satellite_name != None and (d.cod_entity_source, d.cod_entity_target,d.satellite_name, d.num_branch, d.origin_is_incremental, d.origin_is_total, d.origin_is_cdc) not in all_satellites:
                    all_satellites.append((d.cod_entity_source, d.cod_entity_target,d.satellite_name, d.num_branch, d.origin_is_incremental, d.origin_is_total, d.origin_is_cdc))
        return all_satellites

    def get_dv_properties_from_cod_entity_and_num_connection(self,cod_entity, num_connection):
        for d in self.entry_dv_properties:
            if d.cod_entity == cod_entity and int(d.num_connection) == int(num_connection):
                return d
        return None

    def get_all_cod_entity_source_from_cod_entity_target_on_entry_dv(self, cod_entity):
        all_cod_entity = []
        all_entities = []
        for d in self.entry_dv_mappings:
            if d.cod_entity_target == cod_entity and d.cod_entity_source not in all_cod_entity:
                all_cod_entity.append(d.cod_entity_source)
                all_entities.append(d)
        return all_entities

    def get_first_entry_dv_mappings_from_cod_entity_target_and_key_type_and_num_branch(self, cod_entity, key_type, num_branch):
        for d in self.entry_dv_mappings:
            if d.num_branch != num_branch: continue
            if d.cod_entity_target == cod_entity and key_type == d.key_type: return d
        return None

    def get_dict_origin_type_from_cod_entity_on_dv(self, cod_entity):
        source_options = dict()
        source_options['origin_is_cdc'] = 0
        source_options['origin_is_incremental'] = 0
        source_options['origin_is_total'] = 0
        for d in self.entry_dv_mappings:
            if d.cod_entity_target == cod_entity:
                if d.origin_is_cdc == 1: source_options['origin_is_cdc'] = 1
                if d.origin_is_incremental == 1: source_options['origin_is_incremental'] = 1
                if d.origin_is_total == 1: source_options['origin_is_total'] = 1
        return source_options

    def get_list_num_connection_with_driven_key_from_cod_entity_target(self, cod_entity):
        all_connections_with_dk = []
        for d in self.entry_dv_mappings:
            if d.cod_entity_target == cod_entity and d.key_type == KEY_TYPE_DRIVENKEY:
                if d.num_connection not in all_connections_with_dk: all_connections_with_dk.append(d.num_connection)
        return all_connections_with_dk

    def get_om_dataset_file_from_id_dataset(self, id_dataset):
        for d in self.om_dataset_file:
            if d.id_dataset == id_dataset: return d
        return None



