import json
import math
import pickle
from abc import abstractmethod
from pathlib import Path
from typing import Any, Generator, Optional, TextIO, Type, TypeVar, cast

import networkx as nx

from plasnet.ColorPicker import ColorPicker
from plasnet.Templates import Templates
from plasnet.utils import DistanceTags

BaseGraphType = TypeVar("BaseGraphType", bound="BaseGraph")


class BaseGraph(nx.Graph):  # type: ignore
    """
    Class to represent a base class to concentrate common methods
    between the different types of graphs.
    """

    def __init__(self, graph: Optional[nx.Graph] = None, label: str = "") -> None:
        super().__init__(graph)
        self._label = label
        self._path: Optional[Path] = None  # path to html file for visualisation of this graph

    @property
    def label(self) -> str:
        return self._label

    @property
    def path(self) -> Optional[Path]:
        return self._path

    @path.setter
    def path(self, path: Path) -> None:
        self._path = path

    @property
    def description(self) -> str:
        return f"{self.label} ({self.number_of_nodes()} nodes, {self.number_of_edges()} edges)"

    def _get_node_color(self, node: str) -> str:
        return ColorPicker.get_default_color()

    def _get_node_shape(self, node: str) -> str:
        return "circle"

    def _add_special_node_attributes(self, node: str, attrs: dict[str, Any]) -> None:
        ...

    def remove_plasmids(self, plasmids_to_be_removed: list[str]) -> None:
        self.remove_nodes_from(plasmids_to_be_removed)

    def fix_node_attributes(self) -> None:
        for node, attrs in self.nodes.items():
            attrs["color"] = self._get_node_color(node)
            attrs["shape"] = self._get_node_shape(node)
            self._add_special_node_attributes(node, attrs)

    def fix_edge_attributes(self) -> None:
        for edge, attrs in self.edges.items():
            distances = (
                attrs.get(DistanceTags.SplitDistanceTag.value, math.nan),
                attrs.get(DistanceTags.TypeDistanceTag.value, math.nan),
            )
            filtered_distances = filter(lambda x: not math.isnan(x), distances)
            string_distances = map(str, filtered_distances)
            distance_label = " / ".join(string_distances)
            attrs["d_lbl"] = distance_label

    def get_induced_components(self, nodes: list[str]) -> Generator["BaseGraph", None, None]:
        subgraph = self.subgraph(nodes)
        yield from (
            BaseGraph(subgraph.subgraph(component))
            for component in nx.connected_components(subgraph)
        )

    TIME_LIMIT_FOR_SMALL_GRAPHS = 1000
    TIME_LIMIT_FOR_LARGE_GRAPHS = 10000

    def get_simulation_time(self) -> int:
        is_a_small_enough_graph = self.number_of_nodes() <= 5 or self.number_of_edges() <= 10
        if is_a_small_enough_graph:
            return self.TIME_LIMIT_FOR_SMALL_GRAPHS
        else:
            return self.TIME_LIMIT_FOR_LARGE_GRAPHS

    def produce_visualisation(self) -> str:
        self.fix_node_attributes()
        self.fix_edge_attributes()
        visualisation_src = Templates.read_template("visualisation_template")

        graph_as_cy_dict = nx.cytoscape_data(self)
        elements_as_cy_json = json.dumps(graph_as_cy_dict["elements"])

        # [CRITICAL] TODO: improve this horrible performance
        libs_relative_path = self._get_libs_relative_path()
        samples_selectors = self._get_samples_selectors_HTML()
        filters = self._get_filters_HTML()
        custom_buttons = self._get_custom_buttons_HTML()

        final_html_lines = []
        for line in visualisation_src:
            line = line.replace("<libs_relative_path>", libs_relative_path)
            line = line.replace("<samples_selectors>", samples_selectors)
            line = line.replace("<elements_tag>", elements_as_cy_json)
            line = line.replace("<movementThreshold>", str(self.number_of_edges()))
            line = line.replace("<maxSimulationTime>", str(self.get_simulation_time()))
            line = line.replace("<filters_tag>", filters)
            line = line.replace("<custom_buttons_tag>", custom_buttons)
            final_html_lines.append(line)

        return "\n".join(final_html_lines)

    @abstractmethod
    def _get_libs_relative_path(self) -> str:
        ...

    @abstractmethod
    def _get_samples_selectors_HTML(self) -> str:
        ...

    @abstractmethod
    def _get_filters_HTML(self) -> str:
        ...

    @abstractmethod
    def _get_custom_buttons_HTML(self) -> str:
        ...

    def save(self, filepath: Path) -> None:
        with open(filepath, "wb") as fh:
            pickle.dump(self, fh)

    @classmethod
    def load(cls: Type[BaseGraphType], filepath: Path) -> BaseGraphType:
        with open(filepath, "rb") as fh:
            graph = pickle.load(fh)
            return cast(BaseGraphType, graph)

    def write_classification(self, typing_fh: TextIO) -> None:
        for node in self.nodes:
            typing_fh.write(f"{node}\t{self.label}\n")
