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
    
    def same_degree_nodes(self, network: dict) -> dict:
        """Group the nodes with same degrees together"""

        n_ks = {} # Create empty dict to store key degree : values [associated nodes in list]
        node_deg = self.get_node_degrees(network)
        for node, degree in node_deg.items():
            # print(f"{node} has {degree} degrees")
            if degree not in n_ks:
                n_ks[degree] = []
            n_ks[degree].append(node) # `n_ks[degree]` is a list we append all corresponding nodes to

        return n_ks
    
    def degree_distribution(self, network: dict):
        """Get ratio of degree with specific nodes to all nodes"""
        
        p_ks = {} # Create empty dict to store key degree : value distribution %
        degrees = self.same_degree_nodes(network)
        for degree, nodes in degrees.items():
            n_k = len(nodes) # Number of nodes in degree
            n = len(network) # All nodes in network
            p_ks[degree] = n_k / n # At key degree, set the value to the prob
        
        return p_ks