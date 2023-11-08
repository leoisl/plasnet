from plasnet.base_graph import BaseGraph
import networkx as nx
import logging


class BlackholeGraph(BaseGraph):
    """
    This is a class that recognises and labels blackhole plasmids.
    """
    def __init__(self, graph: nx.Graph, blackhole_connectivity_threshold: int, edge_density: float):
        super().__init__(graph)
        self._original_graph = graph
        self._blackhole_connectivity_threshold = blackhole_connectivity_threshold
        self._edge_density = edge_density
        self._blackhole_plasmids = self._get_blackhole_plasmids()

    def _get_node_shape(self, node):
        if node in self._blackhole_plasmids:
            return "star"
        return "circle"

    def _add_special_node_attributes(self, node, attrs):
        if node in self._blackhole_plasmids:
            attrs["is_blackhole"] = True
        else:
            attrs["is_blackhole"] = False

    def _get_blackhole_plasmids(self) -> list["Nodes"]:
        blackhole_plasmids_in_graph = []
        for node in self.nodes:
            if self.degree(node) >= self._blackhole_connectivity_threshold:
                neighbors = list(self.neighbors(node))
                subgraph = nx.induced_subgraph(self._original_graph, neighbors)
                nb_of_edges_between_neighbours = subgraph.number_of_edges()
                max_nb_of_edges_between_neighbours = (len(neighbors) * (len(neighbors) - 1)) // 2
                edge_rate = nb_of_edges_between_neighbours / max_nb_of_edges_between_neighbours
                if edge_rate <= self._edge_density:
                    blackhole_plasmids_in_graph.append(node)
                    logging.debug(f"{node} is a blackhole plasmid, REMOVED")
                else:
                    logging.debug(f"{node} is highly connected but does not connect unrelated plasmids, not removed")
        return blackhole_plasmids_in_graph

    def get_nb_of_blackhole_plasmids(self) -> int:
        return len(self._blackhole_plasmids)

    def remove_blackhole_plasmids(self) -> None:
        self.remove_nodes_from(self._blackhole_plasmids)

    def _get_filters_HTML(self) -> str:
        nb_of_black_holes = len(self._get_blackhole_plasmids())
        return (f'<label for="hide_blackholes">Hide blackhole plasmids ({nb_of_black_holes} present)</label>'
                f'<input type="checkbox" id="hide_blackholes" name="hide_blackholes"><br/>')

    def _get_custom_buttons_HTML(self) -> str:
        return '<div><input type="submit" value="Redraw" onclick="redraw()"></div>'
