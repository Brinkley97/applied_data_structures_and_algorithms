from abc import ABC, abstractmethod

class DataStructureComputationsFactory(ABC):
    """An abstract base class to perform options"""

    def __init__(self):
        pass

class DictionaryComputation(DataStructureComputationsFactory):
    """A class that inherits from DataStructureComputationsFactory."""

    def get_node_degrees(self, network: dict) -> dict: 
        """Get the degree of each node."""
        
        degree_of_each_node = {}

        # `neighbors` is the nodes that belong to the specific `node` of interests
        for node, neighbors in network.items():
            degree_of_each_node[node] = len(neighbors)
                
        return degree_of_each_node
    
    def get_nodes(self, network: dict) -> list:
        """Get the actual nodes in the network."""
        return list(network.keys())

    def total_nodes(self, network: dict) -> int:
        """Get the total #nodes in the network."""
        return len(network)

    def total_links(self, network: dict) -> float:
        """Get the total #links in the network."""

        degrees = self.get_node_degrees(network)

        return sum(degrees.values()) // 2

    def avg_node_degree(self, network: dict) -> float:
        """Compute the average node degree, which is the #neighbors that any node can have on average."""

        total_links = self.total_links(network) * 2 # Count each link 2x
        return total_links / self.total_nodes(network)
    