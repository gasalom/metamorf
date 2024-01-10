from metamorf.engines.engine import Engine
from metamorf.constants import *
from metamorf.tools.manifest import generate_manifest
from metamorf.tools.utils import get_list_nodes_from_metadata

class EngineManifest(Engine):

    def _initialize_engine(self):
        self.engine_name = "Engine Manifest"
        self.engine_command = "manifest"

    def run(self):
        self.start_execution(need_configuration_file=True)
        self.metadata = self.load_metadata(load_om=True, load_entry=False, load_ref=True, load_im=True, owner=self.owner)
        self.log.log(self.engine_name, "Starting the create Manifest File", LOG_LEVEL_INFO)

        all_nodes = get_list_nodes_from_metadata(self.metadata, self.log)
        generate_manifest(self.metadata, self.configuration_file, all_nodes)

        self.log.log(self.engine_name, "Manifest File Finished", LOG_LEVEL_INFO)
        self.finish_execution()




