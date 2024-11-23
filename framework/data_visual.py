import networkx as nx

from abc import ABC, abstractmethod
from data_loader import LoadNetworkX

class VisualizeNetworkFactory(ABC):
    """An abstract base class to load any network"""

    def __init__(self):
        pass

    def dict_to_graph(self):
        pass
    
class VisualizeNetworkX(VisualizeNetworkFactory):
    """A class that inherits from VisualizeNetworkFactory with the utilization of NetworkX"""

    def __init__(self):
        # self.network = LoadNetworkX.dict_to_graph()
        pass
    
    def visualize(self, network: nx.Graph):
        return nx.draw_networkx(network)