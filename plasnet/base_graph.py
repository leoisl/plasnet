from abc import abstractmethod
import networkx as nx


class BaseGraph(nx.Graph):
    """
    Class to represent a base class to concentrate common methods between the different types of graphs.
    """
    @abstractmethod
    def produce_visualisation(self, outdir):
        ...
