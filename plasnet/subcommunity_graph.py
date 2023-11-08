from plasnet.blackhole_graph import BlackholeGraph
import networkx as nx

class SubcommunityGraph(BlackholeGraph):
    def __init__(self, graph: nx.Graph, blackhole_connectivity_threshold: int, edge_density: float, colour: str):
        super().__init__(graph, blackhole_connectivity_threshold, edge_density)
        self._colour = colour

    def _get_libs_relative_path(self) -> str:
        return ".."

    def _get_samples_selectors_HTML(self) -> str:
        return ""

    def _get_node_color(self, node):
        return self._colour
