import networkx as nx
import graph_tool.all as gt

from abc import ABC, abstractmethod

class LoadNetworkFactory(ABC):
    """An abstract base class to load any network"""

    def __init__(self):
        pass

    def dict_to_graph(self):
        pass

class LoadNetworkX(LoadNetworkFactory):
    """A class that inherits from LoadNetworkFactory with the utilization of NetworkX"""
    
    def dict_to_graph(self, network):
        return nx.to_networkx_graph(network)
    
class LoadPyG(LoadNetworkFactory):
    """A class that inherits from LoadNetworkFactory with the utilization of PyG"""

    def dict_to_graph(self):
        pass

class LoadGraphTool(LoadNetworkFactory):
    """A class that inherits from LoadNetworkFactory with the utilization of graph-tool"""

    def dict_to_graph(self, network: dict, directed: bool, all_integers: bool):
        g = gt.Graph(directed=directed)

        if all_integers:
            # Add nodes
            for node in network:
                g.add_vertex(node + 1)  # Ensure all nodes are added

            # Add edges
            for from_node, to_nodes in network.items():
                for to_node in to_nodes:
                    g.add_edge(from_node, to_node)
        else:
            # Prepare edge list
            edge_list = []
            for from_node, to_nodes in network.items():
                for to_node in to_nodes:
                    edge_list.append((from_node, to_node))
            
            # Add edges with hashed=True
            g.add_edge_list(edge_list, hashed=True)

        return g
