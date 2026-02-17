from typing import Optional

import networkx as nx

from plasnet.ColorPicker import ColorPicker
from plasnet.hub_graph import HubGraph


class SubcommunityGraph(HubGraph):
    def __init__(
        self,
        graph: Optional[nx.Graph] = None,
        hub_connectivity_threshold: int = 0,
        edge_density: float = 0.0,
        label: str = "",
        colour: str = ColorPicker.get_default_color(),
    ):
        super().__init__(graph, hub_connectivity_threshold, edge_density, label)
        self._colour = colour

    def _get_libs_relative_path(self) -> str:
        return ".."

    def _get_samples_selectors_HTML(self) -> str:
        return ""

    def _get_node_color(self, node: str) -> str:
        return self._colour
