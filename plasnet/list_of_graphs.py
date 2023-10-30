from base_graph import BaseGraph
import pickle


class ListOfGraphs(list[BaseGraph]):
    def save(self, filepath):
        with open(filepath, "wb") as fh:
            pickle.dump(self, fh)

    @staticmethod
    def load(filepath) -> "ListOfGraphs":
        with open(filepath, "rb") as fh:
            graphs = pickle.load(fh)
            return graphs
