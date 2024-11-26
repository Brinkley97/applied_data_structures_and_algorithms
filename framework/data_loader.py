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

    def generate_rand_dict(self, N: int, directed: bool):
        """Generate a random dictionary representing a graph.

        Parameters:
        -----------
        N: `int`
            Number of nodes in the graph.
        
        directed: 'bool'
            If True, generates a directed graph. 
            If False, generates an undirected graph.

        Returns:
        --------
        rand_dict: `dict`
            A dictionary where each key is a node and its value is a list of connected nodes.
        """

        rand_dict = {}
        domain = list(range(1, N + 1))  # Node labels range from 1 to N (inclusive).

        # Initialize an empty adjacency list for each node.
        for key in domain:
            rand_dict[key] = []

        for key in domain:
            # Exclude self-loops (a node cannot be connected to itself).
            filtered_domain_list = []
            for value in domain:
                if value != key:
                    filtered_domain_list.append(value)

            # Randomize the number of neighbors for the current node.
            max_length = len(filtered_domain_list)
            rand_value_len = np.random.randint(low=1, high=max_length + 1)  # `+1` for inclusiveness

            # Generate unique neighbors for the current node.
            rand_values = np.random.choice(filtered_domain_list, size=rand_value_len, replace=False).tolist()

            # Handle undirected and directed cases.
            if not directed:  # Undirected graph.
                for rand_value in rand_values:
                    if rand_value not in rand_dict[key]:  # Avoid duplicate nodes for same key, thus each value in key is unique
                        rand_dict[key].append(rand_value)
                    if key not in rand_dict[rand_value]:  # Ensure mutual connection.
                        rand_dict[rand_value].append(key)
            elif directed:  # Directed graph.
                for rand_value in rand_values:
                    if rand_value not in rand_dict[key]:  # Add edge from key to rand_value.
                        rand_dict[key].append(rand_value)
            else:
                print(f"Invalid value for directed: {directed}")

        return rand_dict

    # def select_file(self):
    #     """Option if no file is provided, prompt user to select a file"""
    #     file_path = easygui.fileopenbox()
    #     print(f"Selected file: {file_path}")
    #     return file_path
    
class LoadNetworkX(LoadNetworkFactory):
    """A class that inherits from LoadNetworkFactory with the utilization of NetworkX"""
    
    def dict_to_graph(self, network: dict):
        return nx.to_networkx_graph(network)
    
    def load_edge_file(self, file: str = None):
        if file:
            G = nx.read_edgelist(file)
        else:
            pass
            # file_to_load = self.select_file()
            # G = nx.read_edgelist(file_to_load)

        return G
    
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