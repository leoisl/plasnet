import networkx as nx

from plasnet.blackhole_graph import BlackholeGraph
from plasnet.ColorPicker import ColorPicker


class SubcommunityGraph(BlackholeGraph):
    def __init__(
        self,
        graph: nx.Graph = None,
        blackhole_connectivity_threshold: int = 0,
        edge_density: float = 0.0,
        label: str = "",
        colour: str = ColorPicker.get_default_color(),
    ):
        super().__init__(graph, blackhole_connectivity_threshold, edge_density, label)
        self._colour = colour

    def _get_libs_relative_path(self) -> str:
        return ".."

    def _get_samples_selectors_HTML(self) -> str:
        return ""

    def _get_node_color(self, node):
        return self._colour
