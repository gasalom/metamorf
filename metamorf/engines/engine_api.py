from metamorf.engines.engine import Engine
from flask import Flask, Response, json, request
from metamorf.constants import *
from metamorf.tools.manifest import generate_manifest
from metamorf.tools.utils import get_list_nodes_from_metadata
import re


class EndpointDataset(object):

    def __init__(self, manifest):
        self.manifest = manifest

    def __call__(self, **args):
        name_dataset = request.args.get('name')
        if len(args)>0: name_dataset = args['name']
        response = "{}"
        if name_dataset is None: return self.manifest['datasets']
        for pos in self.manifest['datasets']:
            for key, value in pos.items():
                if key.upper() == name_dataset.upper():
                    response = value
        return response


class EndpointNodes(object):

    def __init__(self, manifest):
        self.manifest = manifest

    def __call__(self, **args):
        name_dataset = request.args.get('node')
        if len(args)>0: name_dataset = args['name']
        response = "{}"
        if name_dataset is None: return self.manifest['nodes']
        for pos in self.manifest['nodes']:
                if pos['name'].upper() == name_dataset.upper():
                    response = pos
        return response


class EndpointLineage(object):

    def __init__(self, metadata):
        self.metadata = metadata

    def __call__(self, **args):
        dataset_name = request.args.get('dataset_name')
        column_name = request.args.get('column_name')
        response = dict()
        if len(args)>0:
            dataset_name = args['dataset_name']
            column_name = args['column_name']
        response['name'] = dataset_name
        response['column'] = column_name
        response_origins = []
        if dataset_name is None or column_name is None:
            response['name'] = "Error on INPUT"
            response.pop('column')
            return response
        dataset_spec = self.metadata.get_dataset_spec_from_id_dataset_and_column_name(self.metadata.get_dataset_from_dataset_name(dataset_name).id_dataset,column_name)
        if dataset_spec is None:
            response['column'] = "Column doesn't exist"
            return response

        mapping = self.metadata.get_dataset_t_mapping_from_id_dataset_spec(dataset_spec.id_dataset_spec)
        for map in mapping:
            result = self.replace_mapping(map.value_mapping)
            for r in result:
                new_origin = dict()
                new_origin['branch'] = map.id_branch
                new_origin['origin'] = str(r)

                response_origins.append(new_origin)

        response['source'] = response_origins
        return response

    def replace_mapping(self, mapping):
        all_maps = []
        all_cols = re.findall(r'\[(\d+)\]', mapping)
        for col in all_cols:
            map = self.metadata.get_dataset_t_mapping_from_id_dataset_spec(col)
            if len(map) == 0:
                result = self.metadata.get_tables_dot_column_from_id_dataset_spec(col)
                all_maps.append(mapping.replace("["+col+"]", result))
            else:
                for map_tmp in map:
                    map_tmp = mapping.replace("["+col+"]", map_tmp.value_mapping)
                    map_tmp = self.replace_mapping(map_tmp)
                    all_maps.append(map_tmp)
        return all_maps


class EngineApi(Engine):
    app = None

    def _initialize_engine(self):
        self.engine_name = "Engine API"
        self.engine_command = "api"
        self.app = Flask("Metamorf API")

    def run(self):
        self.start_execution()
        self.metadata = self.load_metadata(load_om=True, load_entry=False, load_ref=True, load_im=True, owner=self.owner)
        all_nodes = get_list_nodes_from_metadata(self.metadata, self.log)
        self.manifest = generate_manifest(self.metadata, self.configuration, all_nodes)

        self.log.log(self.engine_name, "Starting the API Server", LOG_LEVEL_INFO)
        self.add_endpoints()
        self.app.run(host=self.configuration['api']['host'], port=self.configuration['api']['port'])

        self.finish_execution()

    def add_endpoints(self):
        self.app.add_url_rule('/dataset/<string:name>', 'dataset', EndpointDataset(self.manifest))
        self.app.add_url_rule('/dataset', 'dataset_params', EndpointDataset(self.manifest))
        self.app.add_url_rule('/node/<string:name>', 'node', EndpointNodes(self.manifest))
        self.app.add_url_rule('/node', 'node_params', EndpointNodes(self.manifest))
        self.app.add_url_rule('/lineage/<string:dataset_name>/<string:column_name>', 'lineage', EndpointLineage(self.metadata))
        self.app.add_url_rule('/lineage', 'lineage_params', EndpointLineage(self.metadata))




