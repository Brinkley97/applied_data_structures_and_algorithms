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

    def dict_to_graph(self, 
                      network: dict,
                      directed: bool = False,
                      integer_node_ids: bool = False):
        """
        Converts a dictionary to a graph-tool graph.

        Parameters:
        -----------
        network: `dict`
            The input network as an adjacency list.
        directed: `bool`
            Whether the graph is directed.
        integer_node_ids: `bool`
            If True, treat dictionary keys and values as integer node IDs. If False, nodes can be any type (e.g., strings).

        Returns:
        --------
        g: `gt.Graph`
            A graph-tool graph.
        """
        g = gt.Graph(directed=directed)
        node_map = {}  # Maps original node labels to graph-tool vertex indices
        label_prop = g.new_vertex_property("string")  # Property for storing node labels

        if integer_node_ids:
            # Add nodes and edges for integer-only dictionary
            max_node = max(network.keys())  # Ensure vertex indices cover all nodes
            while len(g.get_vertices()) <= max_node:
                g.add_vertex()

            # Add edges
            for from_node, to_nodes in network.items():
                for to_node in to_nodes:
                    g.add_edge(from_node, to_node)
        else:
            # For non-integer nodes, handle with mapping
            current_index = 0

            # Create a mapping from node identifiers to graph-tool vertex indices
            for node in network:
                if node not in node_map:
                    node_map[node] = current_index
                    v = g.add_vertex()
                    label_prop[v] = str(node)  # Store the actual label
                    current_index += 1

                for neighbor in network[node]:
                    if neighbor not in node_map:
                        node_map[neighbor] = current_index
                        v = g.add_vertex()
                        label_prop[v] = str(neighbor)  # Store the actual label
                        current_index += 1

            # Add edges using the node_map
            for from_node, to_nodes in network.items():
                for to_node in to_nodes:
                    g.add_edge(node_map[from_node], node_map[to_node])

        # Assign labels only for non-integer nodes
        if not integer_node_ids:
            g.vertex_properties["label"] = label_prop

        return g