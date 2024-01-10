from metamorf.tools.database_objects import *
from metamorf.tools.query import Query, FromRelationQuery, OrderByQuery
from metamorf.constants import *
from metamorf.tools.metadata import Metadata
from metamorf.tools.connection import Connection
from metamorf.tools.log import Log
from metamorf.tools.node import Node
import re

def Sort_Dataset_Specification_By_Ordinal_Position(sub_list):
    sub_list.sort(key=lambda x: x.ordinal_position)
    return sub_list

def get_metadata_from_database(connection: Connection, log: Log, owner: str, load_om: bool=True, load_ref: bool=True, load_entry: bool=True, load_im: bool=True):

    metadata = Metadata(log)

    query = Query()
    query.set_type(QUERY_TYPE_SELECT)
    log.log("Metadata Loader", "Starting to load Metadata into metamorf", LOG_LEVEL_INFO)

    if load_om:
        where_filter = COLUMN_OM_OWNER + "='" + owner + "'"
        query.set_where_filters(where_filter)

        # OM_DATASET
        log.log("Metadata Loader", "Start to load [OM_DATASET]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET)
        query.set_select_columns(COLUMNS_OM_DATASET)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res= metadata.add_om_dataset(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET]", LOG_LEVEL_DEBUG)

        # OM_DATASET_DV
        log.log("Metadata Loader", "Start to load [OM_DATASET_DV]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_DV)
        query.set_select_columns(COLUMNS_OM_DATASET_DV)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_dv(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_DV]", LOG_LEVEL_DEBUG)

        # OM_DATASET_EXECUTION
        log.log("Metadata Loader", "Start to load [OM_DATASET_EXECUTION]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_EXECUTION)
        query.set_select_columns(COLUMNS_OM_DATASET_EXECUTION)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_execution(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_EXECUTION]", LOG_LEVEL_DEBUG)

        # OM_DATASET_T_ORDER
        log.log("Metadata Loader", "Start to load [OM_DATASET_T_ORDER]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_T_ORDER)
        query.set_select_columns(COLUMNS_OM_DATASET_T_ORDER)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_t_order(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_T_ORDER]", LOG_LEVEL_DEBUG)

        # OM_DATASET_T_AGG
        log.log("Metadata Loader", "Start to load [OM_DATASET_T_AGG]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_T_AGG)
        query.set_select_columns(COLUMNS_OM_DATASET_T_AGG)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_t_agg(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_T_AGG]", LOG_LEVEL_DEBUG)

        # OM_DATASET_T_DISTINCT
        log.log("Metadata Loader", "Start to load [OM_DATASET_T_DISTINCT]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_T_DISTINCT)
        query.set_select_columns(COLUMNS_OM_DATASET_T_DISTINCT)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_t_distinct(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_T_DISTINCT]", LOG_LEVEL_DEBUG)

        # OM_DATASET_T_FILTER
        log.log("Metadata Loader", "Start to load [OM_DATASET_T_FILTER]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_T_FILTER)
        query.set_select_columns(COLUMNS_OM_DATASET_T_FILTER)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_t_filter(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_T_FILTER]", LOG_LEVEL_DEBUG)

        # OM_DATASET_T_HAVING
        log.log("Metadata Loader", "Start to load [OM_DATASET_T_HAVING]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_T_HAVING)
        query.set_select_columns(COLUMNS_OM_DATASET_T_HAVING)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_t_having(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_T_HAVING]", LOG_LEVEL_DEBUG)

        # OM_DATASET_T_MAPPING
        log.log("Metadata Loader", "Start to load [OM_DATASET_T_MAPPING]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_T_MAPPING)
        query.set_select_columns(COLUMNS_OM_DATASET_T_MAPPING)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_t_mapping(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_T_MAPPING]", LOG_LEVEL_DEBUG)

        # OM_DATASET_PATH
        log.log("Metadata Loader", "Start to load [OM_DATASET_PATH]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_PATH)
        query.set_select_columns(COLUMNS_OM_DATASET_PATH)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_path(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_PATH]", LOG_LEVEL_DEBUG)

        # OM_DATASET_SPECIFICATION
        log.log("Metadata Loader", "Start to load [OM_DATASET_SPECIFICATION]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_SPECIFICATION)
        query.set_select_columns(COLUMNS_OM_DATASET_SPECIFICATION)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_specification(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_SPECIFICATION]", LOG_LEVEL_DEBUG)

        # OM_DATASET_RELATIONSHIPS
        log.log("Metadata Loader", "Start to load [OM_DATASET_RELATIONSHIPS]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_RELATIONSHIPS)
        query.set_select_columns(COLUMNS_OM_DATASET_RELATIONSHIPS)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_relationships(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_RELATIONSHIPS]", LOG_LEVEL_DEBUG)

        # OM_DATASET_FILE
        log.log("Metadata Loader", "Start to load [OM_DATASET_FILE]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_FILE)
        query.set_select_columns(COLUMNS_OM_DATASET_FILE)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_file(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_FILE]", LOG_LEVEL_DEBUG)

        # OM_DATASET_HARDCODED
        log.log("Metadata Loader", "Start to load [OM_DATASET_HARDCODED]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_DATASET_HARDCODED)
        query.set_select_columns(COLUMNS_OM_DATASET_HARDCODED)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_hardcoded(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_HARDCODED]", LOG_LEVEL_DEBUG)

        # OM_PROPERTIES
        log.log("Metadata Loader", "Start to load [OM_PROPERTIES]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_PROPERTIES)
        query.set_select_columns(COLUMNS_OM_PROPERTIES)
        query.set_where_filters(None)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_properties(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_PROPERTIES]", LOG_LEVEL_DEBUG)


    if load_ref:
        query.set_where_filters(None)

        # OM_REF_QUERY_TYPE
        log.log("Metadata Loader", "Start to load [OM_REF_QUERY_TYPE]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_REF_QUERY_TYPE)
        query.set_select_columns(COLUMNS_OM_REF_QUERY_TYPE)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_ref_query_type(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_REF_QUERY_TYPE]", LOG_LEVEL_DEBUG)

        # OM_REF_ORDER_TYPE
        log.log("Metadata Loader", "Start to load [OM_REF_ORDER_TYPE]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_REF_ORDER_TYPE)
        query.set_select_columns(COLUMNS_OM_REF_ORDER_TYPE)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_ref_order_type(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_REF_ORDER_TYPE]", LOG_LEVEL_DEBUG)

        # OM_REF_JOIN_TYPE
        log.log("Metadata Loader", "Start to load [OM_REF_JOIN_TYPE]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_REF_JOIN_TYPE)
        query.set_select_columns(COLUMNS_OM_REF_JOIN_TYPE)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_ref_join_type(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_REF_JOIN_TYPE]", LOG_LEVEL_DEBUG)

        # OM_REF_MODULES
        log.log("Metadata Loader", "Start to load [OM_REF_MODULES]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_REF_MODULES)
        query.set_select_columns(COLUMNS_OM_REF_MODULES)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_ref_modules(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_REF_MODULES]", LOG_LEVEL_DEBUG)

        # OM_REF_ENTITY_TYPE
        log.log("Metadata Loader", "Start to load [OM_REF_ENTITY_TYPE]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_REF_ENTITY_TYPE)
        query.set_select_columns(COLUMNS_OM_REF_ENTITY_TYPE)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_ref_entity_type(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_REF_ENTITY_TYPE]", LOG_LEVEL_DEBUG)

        # OM_REF_KEY_TYPE
        log.log("Metadata Loader", "Start to load [OM_REF_KEY_TYPE]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_OM_REF_KEY_TYPE)
        query.set_select_columns(COLUMNS_OM_REF_KEY_TYPE)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_ref_key_type(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_REF_KEY_TYPE]", LOG_LEVEL_DEBUG)

    if load_entry:
        where_filter = COLUMN_ENTRY_OWNER + "='" + owner + "'"
        query.set_where_filters(where_filter)

        # ENTRY_ORDER
        log.log("Metadata Loader", "Start to load [ENTRY_ORDER]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_ORDER)
        query.set_select_columns(COLUMNS_ENTRY_ORDER)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_order(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [ENTRY_ORDER]", LOG_LEVEL_DEBUG)

        # ENTRY_AGGREGATORS
        log.log("Metadata Loader", "Start to load [ENTRY_AGGREGATORS]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_AGGREGATORS)
        query.set_select_columns(COLUMNS_ENTRY_AGGREGATORS)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_aggregators(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [ENTRY_AGGREGATORS]", LOG_LEVEL_DEBUG)

        # ENTRY_FILTERS
        log.log("Metadata Loader", "Start to load [ENTRY_FILTERS]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_FILTERS)
        query.set_select_columns(COLUMNS_ENTRY_FILTERS)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_filters(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [ENTRY_FILTERS]", LOG_LEVEL_DEBUG)

        # ENTRY_HAVING
        log.log("Metadata Loader", "Start to load [ENTRY_FILTERS]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_HAVING)
        query.set_select_columns(COLUMNS_ENTRY_HAVING)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_having(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [ENTRY_FILTERS]", LOG_LEVEL_DEBUG)

        # ENTRY_DATASET_RELATIONSHIPS
        log.log("Metadata Loader", "Start to load [ENTRY_DATASET_RELATIONSHIPS]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_DATASET_RELATIONSHIPS)
        query.set_select_columns(COLUMNS_ENTRY_DATASET_RELATIONSHIPS)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_dataset_relationship(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [ENTRY_DATASET_RELATIONSHIPS]", LOG_LEVEL_DEBUG)

        # ENTRY_ENTITY
        log.log("Metadata Loader", "Start to load [ENTRY_ENTITY]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_ENTITY)
        query.set_select_columns(COLUMNS_ENTRY_ENTITY)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_entity(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [ENTRY_ENTITY]", LOG_LEVEL_DEBUG)

        # ENTRY_PATH
        log.log("Metadata Loader", "Start to load [ENTRY_PATH]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_PATH)
        query.set_select_columns(COLUMNS_ENTRY_PATH)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_path(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [ENTRY_PATH]", LOG_LEVEL_DEBUG)

        # ENTRY_DATASET_MAPPINGS
        log.log("Metadata Loader", "Start to load [ENTRY_DATASET_MAPPINGS]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_DATASET_MAPPINGS)
        query.set_select_columns(COLUMNS_ENTRY_DATASET_MAPPINGS)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_dataset_mappings(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [ENTRY_DATASET_MAPPINGS]", LOG_LEVEL_DEBUG)

        # ENTRY_DV_MAPPINGS
        log.log("Metadata Loader", "Start to load [ENTRY_DV_MAPPINGS]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_DV_MAPPINGS)
        query.set_select_columns(COLUMNS_ENTRY_DV_MAPPINGS)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_dv_mappings(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [ENTRY_DV_MAPPINGS]", LOG_LEVEL_DEBUG)

        # ENTRY_DV_ENTITY
        log.log("Metadata Loader", "Start to load [TABLE_ENTRY_DV_ENTITY]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_DV_ENTITY)
        query.set_select_columns(COLUMNS_ENTRY_DV_ENTITY)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_dv_entity(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [TABLE_ENTRY_DV_ENTITY]", LOG_LEVEL_DEBUG)

        # ENTRY_DV_PROPERTIES
        log.log("Metadata Loader", "Start to load [TABLE_ENTRY_DV_PROPERTIES]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_DV_PROPERTIES)
        query.set_select_columns(COLUMNS_ENTRY_DV_PROPERTIES)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_dv_properties(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [TABLE_ENTRY_DV_PROPERTIES]", LOG_LEVEL_DEBUG)

        # ENTRY_FILES
        log.log("Metadata Loader", "Start to load [TABLE_ENTRY_FILES]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_ENTRY_FILES)
        query.set_select_columns(COLUMNS_ENTRY_FILES)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_entry_files(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [TABLE_ENTRY_FILES]", LOG_LEVEL_DEBUG)

    if load_im:
        where_filter = COLUMN_OM_OWNER + "='" + owner + "'"
        query.set_where_filters(where_filter)

        # OM_DATASET_INFORMATION
        log.log("Metadata Loader", "Start to load [OM_DATASET_INFORMATION]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_IM_OM_DATASET_INFORMATION)
        query.set_select_columns(COLUMNS_OM_DATASET_INFORMATION)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_information(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_INFORMATION]", LOG_LEVEL_DEBUG)

        # OM_RELATIONSHIPS
        log.log("Metadata Loader", "Start to load [OM_RELATIONSHIPS]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_IM_OM_RELATIONSHIPS)
        query.set_select_columns(COLUMNS_OM_RELATIONSHIPS)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_relationships(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_RELATIONSHIPS]", LOG_LEVEL_DEBUG)

        # OM_DATASET_SPECIFICATION_INFORMATION
        log.log("Metadata Loader", "Start to load [OM_DATASET_SPECIFICATION_INFORMATION]", LOG_LEVEL_DEBUG)
        query.set_from_tables(TABLE_IM_OM_DATASET_SPECIFICATION_INFORMATION)
        query.set_select_columns(COLUMNS_OM_DATASET_SPECIFICATION_INFORMATION)
        res = connection.execute(str(query))
        if res is False: return None
        data = connection.get_query_result()
        res = metadata.add_om_dataset_specification_information(data)
        if res is False: return None
        log.log("Metadata Loader", "Finished to load [OM_DATASET_SPECIFICATION_INFORMATION]", LOG_LEVEL_DEBUG)



    log.log("Metadata Loader", "Finished to load Metadata into metamorf", LOG_LEVEL_INFO)
    return metadata

def get_all_sources_and_withs_from_dataset(metadata, dataset):
    # Get Sources
    all_sources = metadata.get_all_source_tables_from_target_table_name(dataset.dataset_name)
    for src in all_sources:
        dataset_src = metadata.get_dataset_from_dataset_name(src)
        if dataset_src.id_entity_type == metadata.get_entity_type_from_entity_type_name(ENTITY_WITH).id_entity_type:
            all_new_sources = get_all_sources_and_withs_from_dataset(metadata, dataset_src)
            for x in all_new_sources:
                x_src = metadata.get_dataset_from_dataset_name(x)
                if x_src.id_entity_type == metadata.get_entity_type_from_entity_type_name(ENTITY_WITH).id_entity_type:
                    all_sources.append(x)


    return all_sources

def get_list_nodes_from_metadata(metadata: Metadata, log: Log):

    log.log("Metadata Nodes", "Start to load all the Nodes", LOG_LEVEL_INFO)
    all_nodes = []
    for dataset in [x for x in metadata.om_dataset if x.end_date is None]:
        if dataset.id_entity_type == metadata.get_entity_type_from_entity_type_name(ENTITY_WITH).id_entity_type or dataset.id_entity_type == metadata.get_entity_type_from_entity_type_name(ENTITY_SRC).id_entity_type: continue
        # Get all sources from dataset: separated on tables/views - withs
        all_sources_names = get_all_sources_and_withs_from_dataset(metadata, dataset)
        from_tables = []
        with_tables = []
        for src in all_sources_names:
            data = metadata.get_dataset_from_dataset_name(src)
            if data.id_entity_type != metadata.get_entity_type_from_entity_type_name(ENTITY_WITH).id_entity_type:
                from_tables.append(src)
            else:
                with_tables.append(src)
                with_to_get_source = metadata.get_dataset_from_dataset_name(src)
                from_tables.extend(get_sources_from_dataset_with(metadata, with_to_get_source))

        if dataset.dataset_name in from_tables: from_tables = [i for i in from_tables if i != dataset.dataset_name]
        from_tables = list(dict.fromkeys(from_tables))


        main_query = get_query_object_from_dataset(dataset, False, metadata)

        for with_table in list(set(with_tables)):
            with_dataset = metadata.get_dataset_from_dataset_name(with_table)
            with_query = get_query_object_from_dataset(with_dataset, True, metadata)
            main_query.add_subquery(with_query)

        all_nodes.append(Node(name=dataset.dataset_name, query=main_query, predecessors=from_tables))

    log.log("Metadata Nodes", "Finished to load the Nodes", LOG_LEVEL_INFO)
    return all_nodes

def get_sources_from_dataset_with(metadata,dataset):
    all_sources_names = get_all_sources_and_withs_from_dataset(metadata, dataset)
    new_sources = []
    for src in all_sources_names:
        data = metadata.get_dataset_from_dataset_name(src)
        if data.id_entity_type != metadata.get_entity_type_from_entity_type_name(ENTITY_WITH).id_entity_type:
            new_sources.append(src)
        else:
            new_sources.extend(get_sources_from_dataset_with(metadata, data))
    return new_sources

def get_query_object_from_dataset(dataset: OmDataset, is_with: bool, metadata: Metadata):

    num_branches = metadata.get_num_branches_from_dataset_name(dataset.dataset_name)
    # INSERT Columns
    insert_columns = []
    for dataset_spec in Sort_Dataset_Specification_By_Ordinal_Position([x for x in metadata.om_dataset_specification if x.end_date is None and x.id_dataset == dataset.id_dataset]):
        insert_columns.append(dataset_spec.column_name)

    # PK Columns
    pk_columns = []
    for dataset_spec in [x for x in metadata.om_dataset_specification if x.end_date is None and x.id_dataset == dataset.id_dataset and x.id_key_type == metadata.get_key_type_from_key_type_name(KEY_TYPE_PRIMARY_KEY).id_key_type]:
        pk_columns.append(metadata.get_tables_dot_column_from_id_dataset_spec(dataset_spec.id_dataset_spec))

    # Create table
    columns_specs = []
    all_dataset_specs_from_dataset = [x for x in metadata.om_dataset_specification if x.end_date is None and x.id_dataset == dataset.id_dataset]
    all_dataset_specs_from_dataset.sort(key=lambda x: x.ordinal_position)
    for dataset_spec in all_dataset_specs_from_dataset:
        length_details = ''
        if dataset_spec.column_length != 0 and dataset_spec.column_length is not None:
            length_details = "(" + str(dataset_spec.column_length) + ")"
        if dataset_spec.column_precision != 0 and dataset_spec.column_precision is not None:
            if dataset_spec.column_scale != 0 and dataset_spec.column_scale is not None:
                length_details = "(" + str(dataset_spec.column_scale) + ","+str(dataset_spec.column_scale)+")"
            else:
                length_details = "(" + str(dataset_spec.column_scale)+ ")"
        columns_specs.append(dataset_spec.column_name + " " + dataset_spec.column_type+length_details)
    query = Query()

    for num_branch in range(0,num_branches):

        from_tables = metadata.get_all_source_tables_from_target_table_name_and_branch(dataset.dataset_name, num_branch+1)
        # Sources and Relationships
        tables_and_relations = []
        for rel in metadata.om_dataset_relationships:
            if rel.end_date is not None: continue
            dataset_spec_master = metadata.get_dataset_spec_from_id_dataset_spec(rel.id_dataset_spec_master)
            dataset_master = metadata.get_dataset_from_id_dataset(dataset_spec_master.id_dataset)
            dataset_spec_detail = metadata.get_dataset_spec_from_id_dataset_spec(rel.id_dataset_spec_detail)
            dataset_detail = metadata.get_dataset_from_id_dataset(dataset_spec_detail.id_dataset)

            if dataset_master.id_entity_type != metadata.get_entity_type_from_entity_type_name(ENTITY_WITH).id_entity_type:
                new_dataset_master = metadata.get_dataset_fqdn_from_dataset_name(dataset_master.dataset_name)
            else:
                new_dataset_master = dataset_master.dataset_name

            if dataset_detail.id_entity_type != metadata.get_entity_type_from_entity_type_name(ENTITY_WITH).id_entity_type:
                new_dataset_detail = metadata.get_dataset_fqdn_from_dataset_name(dataset_detail.dataset_name)
            else:
                new_dataset_detail = dataset_detail.dataset_name

            if new_dataset_master in from_tables and new_dataset_detail in from_tables:
                tables_and_relations.append(
                    FromRelationQuery(new_dataset_master, dataset_spec_master.column_name,
                                      new_dataset_detail, dataset_spec_detail.column_name, rel.id_join_type,
                                      "="))

        # If the source is added on the relationships, is it removed from the FROM Tables
        for relations in tables_and_relations:
            if relations.master_table in from_tables:
                from_tables.remove(relations.master_table)
            if relations.detail_table in from_tables:
                from_tables.remove(relations.detail_table)

        # SELECT Columns
        select_columns = []
        new_dataset = metadata.get_dataset_from_dataset_name(dataset.dataset_name)
        for dataset_spec in Sort_Dataset_Specification_By_Ordinal_Position([x for x in metadata.om_dataset_specification if x.end_date is None and new_dataset.id_dataset == x.id_dataset]):
            dataset_t_mapping = metadata.get_dataset_t_mapping_from_id_branch_and_id_dataset_spec(num_branch+1, dataset_spec.id_dataset_spec)
            if dataset_t_mapping is None: continue # If the mapping on that branch has been closed
            new_select_column = dataset_t_mapping.value_mapping
            all_columns = re.findall(r'\[(\d+)\]', new_select_column)
            for col in all_columns:
                new_select_column = new_select_column.replace("[" + col + "]",
                                                              metadata.get_tables_dot_column_from_id_dataset_spec(col))
            new_select_column += ' AS ' + metadata.get_dataset_spec_from_id_dataset_spec(dataset_t_mapping.id_dataset_spec).column_name
            select_columns.append(new_select_column)


        # DISTINCT option
        is_distinct = False
        for distinct in [x for x in metadata.om_dataset_t_distinct if x.end_date is None]:
            if distinct.id_dataset == dataset.id_dataset and distinct.id_branch == (num_branch+1):
                if distinct.sw_distinct == 1: is_distinct = True

        # ORDER Columns
        all_id_dataset_spec = metadata.get_list_id_dataset_spec_from_dataset_name(dataset.dataset_name)
        order_columns = []
        for order in [x for x in metadata.om_dataset_t_order if x.end_date is None]:
            if order.id_dataset_spec in all_id_dataset_spec and order.id_branch == (num_branch+1):
                order_type = metadata.get_order_type_from_id_order_type(order.id_order_type)
                order_columns.append(
                    OrderByQuery(metadata.get_tables_dot_column_from_id_dataset_spec(order.id_dataset_spec),
                                 order_type.order_type_value))

        # AGG Columns
        agg_columns = []
        for agg in [x for x in metadata.om_dataset_t_agg if x.end_date is None]:
            if agg.id_dataset == dataset.id_dataset and agg.id_branch == (num_branch+1):
                agg_columns.append(metadata.get_tables_dot_column_from_id_dataset_spec(agg.id_dataset_spec))

        # WHERE Filters
        where_filters = []
        for filter in [x for x in metadata.om_dataset_t_filter if x.end_date is None]:
            if filter.id_dataset == dataset.id_dataset and filter.id_branch == (num_branch+1):
                filter_value = filter.value_filter
                all_columns = re.findall(r'\[(\d+)\]', filter.value_filter)
                for col in all_columns:
                    filter_value = filter_value.replace("[" + col + "]",
                                                        metadata.get_tables_dot_column_from_id_dataset_spec(col))
                where_filters.append(filter_value)

        # HAVING Filters
        having_filters = []
        for having in [x for x in metadata.om_dataset_t_having if x.end_date is None]:
            if having.id_dataset == dataset.id_dataset and having.id_branch == (num_branch+1):
                having_value = having.value_having
                all_columns = re.findall(r'\[(\d+)\]', having.value_having)
                for col in all_columns:
                    having_value = having_value.replace("[" + col + "]",
                                                        metadata.get_tables_dot_column_from_id_dataset_spec(col))
                having_filters.append(having_value)

        if not is_with:
            target_table = metadata.get_dataset_fqdn_from_dataset_name(dataset.dataset_name)
        else:
            target_table = dataset.dataset_name

        if num_branch == 0:
            query.set_name_query(target_table)
            query.set_target_table(target_table)
            query.set_columns_and_specs(columns_specs)
            query.set_is_with(is_with)
            if is_with: query.set_type(QUERY_TYPE_SELECT)
            query.set_select_columns(select_columns)
            query.set_from_tables(from_tables)
            query.set_is_distinct(is_distinct)
            query.set_from_tables_and_relations(tables_and_relations)
            query.set_insert_columns(insert_columns)
            query.set_order_by_columns(order_columns)
            query.set_having_filters(having_filters)
            query.set_group_by_columns(agg_columns)
            query.set_primary_key(pk_columns)
            query.set_where_filters(where_filters)
        else:
            query_union = Query()
            query_union.set_name_query(target_table)
            query_union.set_target_table(target_table)
            query_union.set_is_with(False)
            query_union.set_select_columns(select_columns)
            query_union.set_from_tables(from_tables)
            query_union.set_is_distinct(is_distinct)
            query_union.set_from_tables_and_relations(tables_and_relations)
            query_union.set_order_by_columns(order_columns)
            query_union.set_having_filters(having_filters)
            query_union.set_group_by_columns(agg_columns)
            query_union.set_primary_key(pk_columns)
            query_union.set_type(QUERY_TYPE_SELECT)
            query_union.set_where_filters(where_filters)
            if len(select_columns) != 0:
                query.add_unionquery(query_union)

    return query

def get_node_with_with_query_execution_settings(connection, metadata, node, configuration):
    ''' Returns the node object with query execution settings configured '''
    does_table_exists = connection.does_table_exists(node.name, connection.schema, connection.database)
    dataset = metadata.get_dataset_from_dataset_name(node.name)
    id_query_type = metadata.get_dataset_execution_from_id_dataset(dataset.id_dataset).id_query_type
    node.query.set_database(connection.get_connection_type())

    if configuration['modules']['elt']['on_schema_change'] != CONFIG_ON_SCHEMA_CHANGE_IGNORE:
        # Get all Metadata from Database
        id_path = (metadata.get_path_from_database_and_schema(node.query.get_database_target(), node.query.get_schema_target())).id_path
        variable_connection = connection.get_connection_type().lower() + "_database"
        configuration_connection_data = configuration['data']
        configuration_connection_data[variable_connection] = (metadata.get_path_from_id_path(id_path)).database_name
        connection.setup_connection(configuration_connection_data, connection.log)
        table_definition = connection.get_table_columns_definition(node.name)
        all_columns = []
        for col in table_definition:
            all_columns.append((col.column_name, col.column_type))
        node.query.set_columns_in_database(all_columns)

    if id_query_type == QUERY_TYPE_INSERT:
        node.query.set_need_create_table(not does_table_exists)
        node.set_node_type(QUERY_TYPE_INSERT)
    if id_query_type == QUERY_TYPE_VIEW:
        node.set_node_type(QUERY_TYPE_VIEW)
    if does_table_exists and id_query_type == QUERY_TYPE_TRUNCATE_AND_INSERT:
        node.set_node_type(QUERY_TYPE_INSERT)
        node.query.set_is_truncate(True)
    if not does_table_exists and id_query_type == QUERY_TYPE_TRUNCATE_AND_INSERT:
        node.set_node_type(QUERY_TYPE_INSERT)
        node.query.set_need_create_table(True)
        node.query.set_is_truncate(True)
    if does_table_exists and id_query_type == QUERY_TYPE_DROP_AND_INSERT:
        node.set_node_type(QUERY_TYPE_INSERT)
        node.query.set_need_create_table(True)
        node.query.set_need_drop_table(True)
    if not does_table_exists and id_query_type == QUERY_TYPE_DROP_AND_INSERT:
        node.set_node_type(QUERY_TYPE_INSERT)
        node.query.set_need_create_table(True)
    if id_query_type == QUERY_TYPE_DELETE and does_table_exists:
        node.set_node_type(QUERY_TYPE_DELETE)
    if id_query_type == QUERY_TYPE_MERGE and does_table_exists:
        node.set_node_type(QUERY_TYPE_MERGE)
    if not does_table_exists and id_query_type == QUERY_TYPE_MERGE:
        node.set_node_type(QUERY_TYPE_MERGE)
        node.query.set_need_create_table(True)
    if id_query_type == QUERY_TYPE_UPDATE and does_table_exists:
        node.set_node_type(QUERY_TYPE_UPDATE)
    if not does_table_exists and id_query_type == QUERY_TYPE_UPDATE:
        node.set_node_type(QUERY_TYPE_UPDATE)
        node.query.set_need_create_table(True)

    return node

def is_valid_table_name(table_name):
    if re.match('^[A-Za-z0-9_]*$', table_name):
        return True
    return False

def is_valid_column_name(table_name):
    if re.match('^[A-Za-z0-9_]*$', table_name):
        return True
    return False
