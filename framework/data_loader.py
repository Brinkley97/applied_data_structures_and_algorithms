import numpy as np
import networkx as nx
import graph_tool.all as gt

from abc import ABC, abstractmethod

class LoadNetworkFactory(ABC):
    """An abstract base class to load any network"""

    def __init__(self):
        pass

    def dict_to_graph(self):
        pass

    def generate_rand_graph(self):
        pass

    def generate_rand_dict(self, N: int):
        """Generate a random undirected graph"""
        g = {}
        domain = list(range(1, N))
        low, high = domain[0], domain[-1] + 1  # Adjust high for inclusivity

        # Initialize an empty list for each key
        for key in domain:
            g[key] = []

        for key in domain:
            print(f"Processing Key: {key}")
            
            # Create a filtered domain excluding the current key
            filtered_domain_list = []
            for value in domain:
                if value != key:
                    filtered_domain_list.append(value)

            # Randomize the length of values for the current key, ensuring it's not larger than filtered_domain_list
            max_length = len(filtered_domain_list)
            rand_value_len = np.random.randint(low=1, high=max_length + 1)  # `+1` to include max_length as a possibility

            # Generate a list of unique random values
            rand_values = np.random.choice(filtered_domain_list, size=rand_value_len, replace=False).tolist()
            
            # Add to the graph and ensure undirected property
            for value in rand_values:
                if value not in g[key]:
                    g[key].append(value)
                if key not in g[value]:  # Ensure mutual connection
                    g[value].append(key)

            print(g)
            print()

        return g

class LoadNetworkX(LoadNetworkFactory):
    """A class that inherits from LoadNetworkFactory with the utilization of NetworkX"""
    
    def dict_to_graph(self, network: dict):
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