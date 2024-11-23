import networkx as nx

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
    
