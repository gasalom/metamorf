from datetime import datetime
from metamorf.constants import *
from metamorf.tools.filecontroller import FileControllerFactory

def generate_manifest(metadata, configuration, all_nodes):
    manifest = dict()

    file_controller_final = FileControllerFactory().get_file_reader(FILE_TYPE_JSON)
    file_controller_final.set_file_location(ACTUAL_PATH, FILE_MANIFEST)
    file_controller_final.setup_writer(FILE_WRITER_NEW_FILE)


    manifest_metadata = dict()
    manifest_metadata['metamorf_version_software'] = VERSION
    manifest_metadata['metamorf_version_metadata'] = metadata.get_version_from_metadata_database()
    manifest_metadata['generated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    manifest_metadata['metadata_database'] = configuration['metadata']['connection_type']
    manifest_metadata['data_database'] = configuration['data']['connection_type']
    manifest_metadata['project_name'] = configuration['name']

    data_database = configuration['data']
    metadata_database = configuration['metadata']

    nodes = []
    for node in all_nodes:
        new_node = dict()
        new_node['name'] = node.name
        new_node['predecessors'] = node.predecessors
        node.query.set_type(QUERY_TYPE_SELECT)
        new_node['query'] = str(node.query)
        nodes.append(new_node)

    datasets = []
    for dataset in metadata.om_dataset_information:
        d = dict()
        d_info = dict()
        d_info['owner'] = dataset.meta_owner
        d_info['entity_type'] = dataset.entity_type_full_name
        d_info['entity_type_description'] = dataset.entity_type_description
        d_info['module_name'] = dataset.module_name
        d_info['module_full_name'] = dataset.module_full_name
        d_info['module_description'] = dataset.module_description
        d_info['database_name'] = dataset.database_name
        d_info['schema_name'] = dataset.schema_name
        d_info['query_type'] = dataset.query_type_name
        d_info['query_type_description'] = dataset.query_type_description

        d_info['start_date'] = dataset.start_date

        d_relationships = []
        for rel in metadata.om_relationships:
            if rel.master_dataset_name == dataset.dataset_name or rel.detail_dataset_name == dataset.dataset_name:
                d_rel = dict()
                d_rel['master_dataset_name'] = rel.master_dataset_name
                d_rel['master_column_name'] = rel.master_column_name
                d_rel['detail_dataset_name'] = rel.detail_dataset_name
                d_rel['detail_column_name'] = rel.detail_column_name
                d_relationships.append(d_rel)
        d_info['relationships'] = d_relationships

        d_columns = []
        for col in metadata.om_dataset_specification_information:
            if col.dataset_name == dataset.dataset_name:
                d_col = dict()
                d_col['column_name'] = col.column_name
                d_col['column_type'] = col.column_type
                d_col['ordinal_position'] = col.ordinal_position
                d_col['is_nullable'] = col.is_nullable
                d_col['column_length'] = col.column_length
                d_col['column_precision'] = col.column_precision
                d_col['column_scale'] = col.column_scale
                d_columns.append(d_col)
        d_info['columns'] = d_columns

        d[dataset.dataset_name] = d_info
        datasets.append(d)

    manifest['metadata'] = manifest_metadata
    manifest['data_database'] = data_database
    manifest['metadata_database'] = metadata_database
    manifest['nodes'] = nodes
    manifest['datasets'] = datasets

    file_controller_final.write_file(manifest)
    file_controller_final.close()
    return manifest