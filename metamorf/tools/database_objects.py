import datetime


# METADATA - Entry Tables
class EntryOrder:

    def __init__(self, cod_entity_target: str, cod_entity_src:str, column_name: str,num_branch: int, order_type: str, owner: str):
        self.cod_entity_target = cod_entity_target
        self.cod_entity_src = cod_entity_src
        self.column_name = column_name
        self.num_branch = num_branch
        self.order_type = order_type
        self.owner = owner

    def get(self):
        return [self.cod_entity_target,self.cod_entity_src, self.column_name, self.num_branch, self.order_type, self.owner]

    def __str__(self):
        return "'"+self.cod_entity_target+"','"+self.cod_entity_src+"','"+self.column_name.replace("'","''")+"',"+str(self.num_branch)+",'"+self.order_type+"','"+self.owner+"'"


class EntryAggregators:

    def __init__(self, cod_entity_target: str, cod_entity_src:str, column_name: str, num_branch: int, owner: str):
        self.cod_entity_target = cod_entity_target
        self.cod_entity_src = cod_entity_src
        self.column_name = column_name
        self.num_branch = num_branch
        self.owner = owner

    def get(self):
        return [self.cod_entity_target,self.cod_entity_src, self.column_name, self.num_branch, self.owner]

    def __str__(self):
        return "'"+self.cod_entity_target+"','"+self.cod_entity_src+"','"+self.column_name.replace("'","''")+"',"+str(self.num_branch)+",'"+self.owner+"'"


class EntryFilters:

    def __init__(self, cod_entity_target: str, value: str, num_branch: int, owner: str):
        self.cod_entity_target = cod_entity_target
        self.value = value
        self.num_branch = num_branch
        self.owner = owner

    def get(self):
        return [self.cod_entity_target, self.value, self.num_branch, self.owner]

    def __str__(self):
        return "'"+self.cod_entity_target+"','"+self.value.replace("'","''")+"',"+str(self.num_branch)+",'"+self.owner+"'"


class EntryHaving:

    def __init__(self, cod_entity_target: str, value: str, num_branch: int, owner: str):
        self.cod_entity_target = cod_entity_target
        self.value = value
        self.num_branch = num_branch
        self.owner = owner

    def get(self):
        return [self.cod_entity_target, self.value, self.num_branch, self.owner]

    def __str__(self):
        return "'"+self.cod_entity_target+"','"+self.value.replace("'","''")+"',"+str(self.num_branch)+",'"+self.owner+"'"


class EntryDatasetRelationships:

    def __init__(self, cod_entity_master: str, column_name_master: str, cod_entity_detail: str, column_name_detail: str, relationship_type: str, owner: str):
        self.cod_entity_master = cod_entity_master
        self.column_name_master = column_name_master
        self.cod_entity_detail = cod_entity_detail
        self.column_name_detail = column_name_detail
        self.relationship_type = relationship_type
        self.owner = owner

    def get(self):
        return [self.cod_entity_master, self.column_name_master, self.cod_entity_detail, self.column_name_detail, self.relationship_type, self.owner]

    def __str__(self):
        return "'"+self.cod_entity_master+"','"+self.column_name_master.replace("'","''")+"','"+self.cod_entity_detail+"','"+self.column_name_detail.replace("'","''")+"','"+self.relationship_type+"','"+self.owner+"'"


class EntryEntity:

    def __init__(self, cod_entity: str, table_name: str, entity_type: str, cod_path: str, strategy: str, owner: str):
        self.cod_entity = cod_entity
        self.table_name = table_name
        self.entity_type = entity_type
        self.cod_path = cod_path
        self.strategy = strategy
        self.owner = owner

    def get(self):
        return [self.cod_entity, self.table_name, self.entity_type, self.cod_path, self.strategy, self.owner]

    def __str__(self):
        return "'"+self.cod_entity+"','"+self.table_name+"','"+self.entity_type+"','"+self.cod_path+"','"+self.strategy+"','"+self.owner+"'"


class EntryPath:

    def __init__(self, cod_path: str, database_name: str, schema_name: str, owner: str):
        self.cod_path = cod_path
        self.database_name = database_name
        self.schema_name = schema_name
        self.owner = owner

    def get(self):
        return [self.cod_path, self.database_name, self.schema_name, self.owner]

    def __str__(self):
        database_name = 'NULL'
        if self.database_name is not None and self.database_name != '': database_name = "'"+self.database_name + "'"
        schema_name = 'NULL'
        if self.schema_name is not None and self.schema_name != '': schema_name = "'" + self.schema_name + "'"
        return "'"+self.cod_path+"'," + database_name+","+schema_name+",'"+self.owner + "'"


class EntryFiles:

    def __init__(self, cod_entity: str, file_path: str, file_name: str, delimiter_character: str, owner: str):
        self.cod_entity = cod_entity
        self.file_path = file_path
        self.file_name = file_name
        self.delimiter_character = delimiter_character
        self.owner = owner

    def get(self):
        return [self.cod_entity, self.file_path, self.file_name, self.delimiter_character, self.owner]

    def __str__(self):
        delimiter_character = 'NULL'
        if self.delimiter_character is not None and self.delimiter_character != '': delimiter_character = "'"+self.delimiter_character + "'"
        return "'"+self.cod_entity+"','" + self.file_path + "','" + self.file_name+"',"+delimiter_character+",'"+self.owner + "'"


class EntryDatasetMappings:

    def __init__(self, cod_entity_source: str, value_source: str, cod_entity_target: str, column_name_target: str, column_type_target: str, ordinal_position: int, column_length : int, column_precision: int, num_branch: int, key_type: str, sw_distinct: int, owner: str):
        if key_type is None or key_type == '': key_type = 'NULL'
        self.cod_entity_source = cod_entity_source
        self.value_source = value_source
        self.cod_entity_target = cod_entity_target
        self.column_name_target = column_name_target
        self.column_type_target = column_type_target
        self.ordinal_position = ordinal_position
        self.column_length = column_length
        self.column_precision = column_precision
        self.num_branch = num_branch
        self.key_type = key_type
        self.sw_distinct = sw_distinct
        self.owner = owner

    def get(self):
        return [self.cod_entity_source, self.value_source, self.cod_entity_target, self.column_name_target,
                self.column_type_target, self.ordinal_position, self.column_length, self.column_precision, self.num_branch,
                self.key_type, self.sw_distinct, self.owner]

    def __str__(self):
        key_type = 'NULL'
        if self.key_type is not None and self.key_type != '': key_type = "'"+self.key_type+"'"
        return "'"+self.cod_entity_source+"','"+self.value_source.replace("'","''")+"','"+self.cod_entity_target+"','" + self.column_name_target+"','"+self.column_type_target+"',"+str(self.ordinal_position) + "," + str(self.column_length)+","+str(self.column_precision)+","+str(self.num_branch)+","+key_type+","+str(self.sw_distinct)+",'"+self.owner+"'"


class EntryDvMappings:

    def __init__(self, cod_entity_source, column_name_source, cod_entity_target,column_name_target, column_type_target, ordinal_position, column_length, column_precision, num_branch,num_connection, key_type, satellite_name, origin_is_incremental, origin_is_total, origin_is_cdc, owner):
        self.cod_entity_source = cod_entity_source
        self.column_name_source = column_name_source
        self.cod_entity_target = cod_entity_target
        self.column_name_target = column_name_target
        self.column_type_target = column_type_target
        self.ordinal_position = ordinal_position
        self.column_length = column_length
        self.column_precision = column_precision
        self.num_branch = num_branch
        self.num_connection = num_connection
        self.key_type = key_type
        self.satellite_name = satellite_name
        self.origin_is_incremental = origin_is_incremental
        self.origin_is_total = origin_is_total
        self.origin_is_cdc = origin_is_cdc
        self.owner = owner

    def get(self):
        return [self.cod_entity_source, self.column_name_source, self.cod_entity_target, self.column_name_target,self.column_type_target,self.ordinal_position,self.column_length, self.column_precision,self.num_branch, self.num_connection, self.key_type,self.satellite_name,self.origin_is_incremental, self.origin_is_total, self.origin_is_cdc, self.owner]

    def __str__(self):
        return "'" + self.cod_entity_source +"','"+self.column_name_source.replace("'","''")+"','"+self.cod_entity_target+"','"+self.column_name_target+"','"+self.column_type_target+"',"+str(self.ordinal_position)+","+str(self.column_length)+\
                ","+str(self.column_precision) + ","+ str(self.num_branch)+","+str(self.num_connection)+",'"+self.key_type+"','"+self.satellite_name+"',"+str(self.origin_is_incremental)+","+str(self.origin_is_total)+","+str(self.origin_is_cdc)+",'"+self.owner+"'"


class EntryDvEntry:

    def __init__(self, cod_entity, entity_name, entity_type, cod_path, name_status_tracking_satellite, name_record_tracking_satellite,
                name_effectivity_satellite, owner):
        if name_status_tracking_satellite is None: name_status_tracking_satellite = ''
        if name_record_tracking_satellite is None: name_record_tracking_satellite = ''
        if name_effectivity_satellite is None: name_effectivity_satellite = ''
        self.cod_entity = cod_entity
        self.entity_name = entity_name
        self.entity_type = entity_type
        self.cod_path = cod_path
        self.name_status_tracking_satellite = name_status_tracking_satellite
        self.name_record_tracking_satellite = name_record_tracking_satellite
        self.name_effectivity_satellite = name_effectivity_satellite
        self.owner = owner

    def get(self):
        return[self.cod_entity, self.entity_name, self.entity_type, self.cod_path, self.name_status_tracking_satellite,self.name_record_tracking_satellite,self.name_effectivity_satellite, self.owner]

    def __str__(self):
        return "'"+self.cod_entity+"','"+self.entity_name+"','"+self.entity_type+"','"+self.cod_path+"','"+self.name_status_tracking_satellite+"','"+self.name_record_tracking_satellite+"',"+ \
               "'"+self.name_effectivity_satellite+"','"+self.owner+"'"


class EntryDvProperties:

    def __init__(self, cod_entity, num_connection, hash_name, owner):
        self.cod_entity = cod_entity
        self.num_connection = num_connection
        self.hash_name = hash_name
        self.owner = owner

    def get(self):
        return [self.cod_entity, self.num_connection, self.hash_name, self.owner]

    def __str__(self):
        return "'" + self.cod_entity + "'," + self.num_connection + ",'" + self.hash_name + "','" + self.owner + "'"


# METADATA - Metamorf Tables
class OmDataset:

    def __init__(self, id_dataset, dataset_name, id_entity_type, id_path, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_dataset = id_dataset
        self.dataset_name = dataset_name
        self.id_entity_type = id_entity_type
        self.id_path = id_path
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_dataset, self.dataset_name, self.id_entity_type, self.id_path, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_dataset) + ",'" + self.dataset_name + "'," + str(self.id_entity_type) + "," + str(self.id_path) + ",'" + self.meta_owner + "'," + self.start_date + "," + end_date


class OmDatasetDv:

    def __init__(self, id_dataset, id_entity_type, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_dataset =  id_dataset
        self.id_entity_type = id_entity_type
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_dataset, self.id_entity_type, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_dataset) + ","+ str(self.id_entity_type) +",'"+self.meta_owner +"'," + self.start_date + "," + end_date


class OmDatasetSpecification:

    def __init__(self, id_dataset_spec, id_dataset, id_key_type, column_name, column_type, ordinal_position, is_nullable, column_length, column_precision, column_scale, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_dataset_spec = id_dataset_spec
        self.id_dataset = id_dataset
        self.id_key_type = id_key_type
        self.column_name = column_name
        self.column_type = column_type
        self.ordinal_position = ordinal_position
        self.is_nullable = is_nullable
        self.column_length = column_length
        self.column_precision = column_precision
        self.column_scale = column_scale
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_dataset_spec, self.id_dataset, self.id_key_type, self.column_name, self.column_type, self.ordinal_position, self.is_nullable, self.column_length, self.column_precision, self.column_scale, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_dataset_spec) + ","+ str(self.id_dataset)+","+str(self.id_key_type)+",'"+str(self.column_name)+"','"+str(self.column_type)+"',"+str(self.ordinal_position)+","+str(self.is_nullable)+","+str(self.column_length)+","+str(self.column_precision)+","+str(self.column_scale)+",'"+str(self.meta_owner) + "'," + self.start_date + "," + end_date


class OmDatasetTAgg:

    def __init__(self, id_t_agg, id_dataset, id_branch, id_dataset_spec, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_t_agg = id_t_agg
        self.id_dataset = id_dataset
        self.id_branch = id_branch
        self.id_dataset_spec = id_dataset_spec
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_t_agg, self.id_dataset, self.id_branch, self.id_dataset_spec, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_t_agg) + "," + str(self.id_dataset) + "," + str(self.id_branch) + ","+ str(self.id_dataset_spec) + ",'" + self.meta_owner + "'," + self.start_date + "," + end_date


class OmDatasetTOrder:

    def __init__(self, id_t_order, id_dataset, id_branch, id_dataset_spec, id_order_type, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_t_order = id_t_order
        self.id_dataset = id_dataset
        self.id_branch = id_branch
        self.id_dataset_spec = id_dataset_spec
        self.id_order_type = id_order_type
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_t_order, self.id_dataset, self.id_branch, self.id_dataset_spec, self.id_order_type, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_t_order)+","+str(self.id_dataset)+","+str(self.id_branch)+","+str(self.id_dataset_spec)+","+str(self.id_order_type)+",'"+self.meta_owner+"',"+self.start_date+","+end_date


class OmDatasetTDistinct:

    def __init__(self, id_t_distinct, id_dataset, id_branch, sw_distinct, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_t_distinct = id_t_distinct
        self.id_dataset = id_dataset
        self.id_branch = id_branch
        self.sw_distinct = sw_distinct
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_t_distinct, self.id_dataset, self.id_branch, self.sw_distinct, self.meta_owner,  self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_t_distinct)+","+str(self.id_dataset)+","+str(self.id_branch)+","+str(self.sw_distinct)+",'"+str(self.meta_owner)+"',"+self.start_date+","+end_date


class OmDatasetExecution:

    def __init__(self, id_dataset, id_query_type, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_dataset = id_dataset
        self.id_query_type = id_query_type
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_dataset, self.id_query_type, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_dataset)+","+str(self.id_query_type)+",'"+self.meta_owner+"',"+self.start_date+","+end_date


class OmProperties:

    def __init__(self, property, value, start_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        self.property = property
        self.value = value
        self.start_date = start_date

    def get(self):
        return [self.property, self.value, self.start_date]

    def __str__(self):
        return "'"+self.property+"','"+self.value+"',"+self.start_date+""


class OmDatasetRelationships:

    def __init__(self, id_relationship, id_dataset_spec_master, id_dataset_spec_detail, id_join_type, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_relationship = id_relationship
        self.id_dataset_spec_master = id_dataset_spec_master
        self.id_dataset_spec_detail = id_dataset_spec_detail
        self.id_join_type = id_join_type
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_relationship, self.id_dataset_spec_master, self.id_dataset_spec_detail, self.id_join_type, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_relationship)+","+str(self.id_dataset_spec_master)+","+str(self.id_dataset_spec_detail)+","+str(self.id_join_type)+",'"+self.meta_owner+"',"+self.start_date+","+end_date


class OmDatasetTMapping:

    def __init__(self, id_t_mapping, id_branch, id_dataset_spec, value_mapping, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_t_mapping = id_t_mapping
        self.id_branch = id_branch
        self.id_dataset_spec = id_dataset_spec
        self.value_mapping = value_mapping
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_t_mapping, self.id_branch, self.id_dataset_spec, self.value_mapping, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_t_mapping)+","+str(self.id_branch)+","+str(self.id_dataset_spec)+",'"+self.value_mapping.replace("'","''")+"','"+self.meta_owner+"',"+self.start_date+","+end_date


class OmDatasetPath:

    def __init__(self, id_path, database_name, schema_name, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_path = id_path
        self.database_name = database_name
        self.schema_name = schema_name
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_path, self.database_name, self.schema_name, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.database_name != None and self.database_name != '': database = "'"+self.database_name+"'"
        else: database = "NULL"
        if self.schema_name != None and self.schema_name != '': schema = "'"+self.schema_name+"'"
        else: schema = "NULL"
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_path)+","+database+","+schema+",'"+self.meta_owner+"',"+self.start_date+","+end_date


class OmDatasetFile:

    def __init__(self, id_dataset, file_path, file_name, delimiter_character, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_dataset = id_dataset
        self.file_path = file_path
        self.file_name = file_name
        self.delimiter_character = delimiter_character
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_dataset, self.file_path ,self.file_name ,self.delimiter_character ,self.meta_owner ,self.start_date ,self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_dataset)+",'"+str(self.file_path)+"','"+self.file_name+"','"+str(self.delimiter_character)+"','"+self.meta_owner+"',"+self.start_date +","+end_date


class OmDatasetTFilter:

    def __init__(self, id_t_filter, id_dataset, id_branch, value_filter, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_t_filter = id_t_filter
        self.id_dataset = id_dataset
        self.id_branch = id_branch
        self.value_filter = value_filter
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_t_filter, self.id_dataset, self.id_branch, self.value_filter, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_t_filter)+","+str(self.id_dataset)+","+str(self.id_branch)+",'"+self.value_filter.replace("'","''")+"','"+self.meta_owner+"',"+self.start_date+","+end_date


class OmDatasetTHaving:

    def __init__(self, id_t_having, id_dataset, id_branch, value_having, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_t_having = id_t_having
        self.id_dataset = id_dataset
        self.id_branch = id_branch
        self.value_having = value_having
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_t_having, self.id_dataset, self.id_branch, self.value_having, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_t_having)+","+str(self.id_dataset)+","+str(self.id_branch)+",'"+self.value_having+"','"+self.meta_owner+"',"+self.start_date+","+end_date


class OmDatasetHardcoded:

    def __init__(self, id_dataset_hardcoded, id_dataset, id_branch, content, meta_owner, start_date, end_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, datetime.datetime): end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        self.id_dataset_hardcoded = id_dataset_hardcoded
        self.id_dataset = id_dataset
        self.id_branch = id_branch
        self.content = content
        self.meta_owner = meta_owner
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        return [self.id_dataset_hardcoded, self.id_dataset, self.id_branch, self.content, self.meta_owner, self.start_date, self.end_date]

    def __str__(self):
        if self.end_date is None or self.end_date == '' or self.end_date=='NULL': end_date = "NULL"
        else: end_date = self.end_date
        return str(self.id_dataset_hardcoded)+","+str(self.id_dataset)+","+str(self.id_branch)+",'"+self.content+"','"+self.meta_owner+"',"+self.start_date+","+end_date

        # METADATA - Reference Tables


class OmRefQueryType:

    def __init__(self, id_query_type, query_type_name, query_type_description):
        self.id_query_type = id_query_type
        self.query_type_name = query_type_name
        self.query_type_description = query_type_description


class OmRefOrderType:

    def __init__(self, id_order_type, order_type_name, order_type_value, order_type_description):
        self.id_order_type = id_order_type
        self.order_type_name = order_type_name
        self.order_type_value = order_type_value
        self.order_type_description = order_type_description


class OmRefJoinType:

    def __init__(self, id_join_type, join_name, join_value, join_description):
        self.id_join_type = id_join_type
        self.join_name = join_name
        self.join_value = join_value
        self.join_description = join_description


class OmRefKeyType:

    def __init__(self, id_key_type, key_type_name, key_type_description):
        self.id_key_type = id_key_type
        self.key_type_name = key_type_name
        self.key_type_description = key_type_description


class OmRefEntityType:

    def __init__(self, id_entity_type, entity_type_name, entity_type_description, entity_type_full_name, id_module):
        self.id_entity_type = id_entity_type
        self.entity_type_name = entity_type_name
        self.entity_type_description = entity_type_description
        self.entity_type_full_name = entity_type_full_name
        self.id_module = id_module


class OmRefModules:

    def __init__(self, id_module, module_name, module_full_name, module_description):
        self.id_module = id_module
        self.module_name = module_name
        self.module_full_name = module_full_name
        self.module_description = module_description


# IM Tables
class OmDatasetInformation:

    def __init__(self, meta_owner, entity_type_full_name, entity_type_description, module_name, module_full_name, module_description, dataset_name, database_name, schema_name, query_type_name, query_type_description, start_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d, %H:%M:%S")
        self.meta_owner = meta_owner
        self.entity_type_full_name = entity_type_full_name
        self.entity_type_description = entity_type_description
        self.module_name = module_name
        self.module_full_name = module_full_name
        self.module_description = module_description
        self.dataset_name = dataset_name
        self.database_name = database_name
        self.schema_name = schema_name
        self.query_type_name = query_type_name
        self.query_type_description = query_type_description
        self.start_date = start_date


class OmRelationships:

    def __init__(self, meta_owner, master_database_name, master_schema_name, master_dataset_name, master_column_name, detail_database_name, detail_schema_name, detail_dataset_name, detail_column_name, start_date):
        if isinstance(start_date, datetime.datetime): start_date = start_date.strftime("%Y-%m-%d, %H:%M:%S")
        self.meta_owner = meta_owner
        self.master_database_name = master_database_name
        self.master_schema_name = master_schema_name
        self.master_dataset_name = master_dataset_name
        self.master_column_name = master_column_name
        self.detail_database_name = detail_database_name
        self.detail_schema_name = detail_schema_name
        self.detail_dataset_name = detail_dataset_name
        self.detail_column_name = detail_column_name
        self.start_date = start_date


class OmDatasetSpecificationInformation:

    def __init__(self, meta_owner, dataset_name, column_name, column_type, ordinal_position, is_nullable, column_length, column_precision, column_scale):
        self.meta_owner = meta_owner
        self.dataset_name = dataset_name
        self.column_name = column_name
        self.column_type = column_type
        self.ordinal_position = ordinal_position
        self.is_nullable = is_nullable
        self.column_length = column_length
        self.column_precision = column_precision
        self.column_scale = column_scale


class Column:

    def __init__(self, id, column_name, column_type, default_value, key_type, is_nullable, column_length, column_precision, column_scale):
        self.id = id
        self.column_name = column_name
        self.column_type = column_type
        self.default_value = default_value
        self.key_type = key_type
        self.is_nullable = is_nullable
        self.column_length = column_length
        self.column_precision = column_precision
        self.column_scale = column_scale

    def __str__(self):
        return str(self.id) + "," + str(self.column_name) +"," + str(self.column_type) +"," + str(self.default_value) +"," + str(self.key_type) + "," + self.is_nullable + "," + self.column_length + "," + self.column_precision + "," + self.column_scale







