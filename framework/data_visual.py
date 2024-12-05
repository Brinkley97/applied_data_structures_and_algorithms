import networkx as nx
import graph_tool.all as gt
import graph_tool.draw as gtd
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod
from data_loader import LoadNetworkX

class VisualizeNetworkFactory(ABC):
    """An abstract base class to load any network"""

    def __init__(self):
        pass

    def dict_to_graph(self):
        pass

    def visualize_graph_evolution(self):
        pass

    
class VisualizeNetworkX(VisualizeNetworkFactory):
    """A class that inherits from VisualizeNetworkFactory with the utilization of NetworkX"""


    def visualize(self, network: nx.Graph):
        """Visualizes a NetworkX graph with or without arrows based on its type (directed/undirected)."""
        if nx.is_directed(network):
            nx.draw_networkx(network, arrows=True, node_size=500, node_color="lightblue")
        else:
            nx.draw_networkx(network, arrows=False, node_size=500, node_color="lightblue")
    
    # def draw_graph(self,network, pos, ax, title):
    #     nx.draw(network, pos, with_labels=True, ax=ax, node_color='lightblue', edge_color='gray')
    #     ax.set_title(title)

    def visualize_graph_evolution(self, network: dict):
        """Visualizes a NetworkX dynamic graph with or without arrows based on its type (directed/undirected)."""

        fig, axes = plt.subplots(1, len(network), figsize=(15, 5))
        pos = None

        for i, (time_step, edges) in enumerate(network.items()):
            G = nx.Graph()
            for node, neighbors in edges.items():
                for neighbor in neighbors:
                    G.add_edge(node, neighbor)
            if pos is None:
                pos = nx.spring_layout(G)  # Compute layout only once
            
            nx.draw(G, pos, with_labels=True, ax=axes[i], node_color='lightblue', edge_color='gray')
            axes[i].set_title(f"Time Step {time_step}")

        plt.show()

class VisualizeGraphTool(VisualizeNetworkFactory):
    """A class that inherits from VisualizeNetworkFactory with the utilization of graph-tool"""

    def visualize(self, 
                  network: gt.Graph,
                  integer_node_ids: bool = False,
                  output_file: str = None):
        """Visualizes the graph-tool graph.

        Parameters:
        ------------
        network: `gt.Graph`
            The graph-tool graph to be visualized.
        
        integer_node_ids: `bool`
            If True, display integer node IDs. If False, display actual node labels.

        output_file: `str`, optional
            File path to save the visualization; if None, it displays the graph interactively.

        """
        # Handle layout
        pos = gtd.sfdp_layout(network)  # Default layout for graph-tool

        # Use actual labels if they exist and integer_node_ids is False
        if not integer_node_ids and "label" in network.vertex_properties:
            label_prop = network.vertex_properties["label"]
        else:
            label_prop = network.vertex_index  # Fallback to vertex indices

        # Remove duplicate edges for bidirectional relationships in undirected graphs
        if not network.is_directed():
            network.set_edge_filter(None)  # Remove any existing filters
            network.set_edge_filter(network.new_edge_property("bool", val=True))

        # Visualize the graph
        if output_file:
            gtd.graph_draw(network, pos, vertex_text=label_prop, output=output_file)
        else:
            gtd.graph_draw(network, pos, vertex_text=label_prop, output_size=(500, 500))