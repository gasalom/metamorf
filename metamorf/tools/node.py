from metamorf.tools.query import Query
from metamorf.constants import *
import time

class Node:

    def __init__(self, name: str, query: Query, predecessors: list[str]):
        '''Name: Name of the process / table that will be loaded
        Query: Process to be executed, need to set the QUERY_TYPE that will be generated
        Predecessors: list string of the predecessors Nodes.name
        '''
        self.query = query
        self.predecessors = predecessors
        self.name = name
        self.status = NODE_STATUS_WAITING
        self.time = 0
        self.id = -1

    def set_node_id(self, id):
        self.id = id

    def set_node_type(self, node_type: int):
        self.query.set_type(node_type)

    def init_execution(self):
        self.time = float(time.time())

    def finish_execution(self):
        self.time = float(time.time()) - float(self.time)
