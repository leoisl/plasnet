import pickle
from pathlib import Path
from typing import Generator, cast

from plasnet.base_graph import BaseGraphType


class ListOfGraphs(list[BaseGraphType]):
    def save(self, filepath: Path) -> None:
        with open(filepath, "wb") as fh:
            pickle.dump(self, fh)

    @classmethod
    def load(cls, filepath: Path) -> "ListOfGraphs[BaseGraphType]":
        with open(filepath, "rb") as fh:
            graphs = pickle.load(fh)
            return cast(ListOfGraphs[BaseGraphType], graphs)

    def _get_each_graph_as_list_of_nodes_in_text_format(
        self,
    ) -> Generator[str, None, None]:
        for graph in self:
            yield " ".join(graph)

    def save_graph_as_text(self, filepath: Path) -> None:
        with open(filepath, "w") as fh:
            for graph_as_text in self._get_each_graph_as_list_of_nodes_in_text_format():
                print(graph_as_text, file=fh)

    def save_classification(self, filepath: Path, header: str) -> None:
        with open(filepath, "w") as fh:
            print(header, file=fh)
            for subgraph in self:
                subgraph.write_classification(fh)

    def get_graphs_sorted_by_size(self) -> "ListOfGraphs[BaseGraphType]":
        return ListOfGraphs(sorted(self, key=lambda graph: graph.number_of_nodes(), reverse=True))
