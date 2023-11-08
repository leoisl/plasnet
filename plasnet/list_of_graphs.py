from plasnet.base_graph import BaseGraph
import pickle
from typing import Generator, TypeVar, Type
from pathlib import Path


BaseGraphT = TypeVar('BaseGraphT', bound=BaseGraph)
ListOfGraphsT = TypeVar('ListOfGraphsT', bound="ListOfGraphs")

class ListOfGraphs(list[BaseGraphT]):


    def save(self, filepath: Path) -> None:
        with open(filepath, "wb") as fh:
            pickle.dump(self, fh)

    @classmethod
    def load(cls: Type[ListOfGraphsT], filepath: Path) -> ListOfGraphsT:
        with open(filepath, "rb") as fh:
            graphs = pickle.load(fh)
            return graphs

    def _get_each_graph_as_list_of_nodes_in_text_format(self) -> Generator[str, None, None]:
        for graph in self:
            yield " ".join(graph)

    def save_graph_as_text(self, filepath: Path) -> None:
        with open(filepath, "w") as fh:
            for graph_as_text in self._get_each_graph_as_list_of_nodes_in_text_format():
                print(graph_as_text, file=fh)
