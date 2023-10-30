from base_graph import BaseGraph
import pickle
from typing import Generator


class ListOfGraphs(list[BaseGraph]):
    def save(self, filepath):
        with open(filepath, "wb") as fh:
            pickle.dump(self, fh)

    @staticmethod
    def load(filepath) -> "ListOfGraphs":
        with open(filepath, "rb") as fh:
            graphs = pickle.load(fh)
            return graphs

    def _get_each_graph_as_list_of_nodes_in_text_format(self) -> Generator[str, None, None]:
        for graph in self:
            yield " ".join(graph)

    def save_graph_as_text(self, filepath):
        with open(filepath, "w") as fh:
            for graph_as_text in self._get_each_graph_as_list_of_nodes_in_text_format():
                print(graph_as_text, file=fh)
