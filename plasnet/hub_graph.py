import logging
from typing import Any, Optional

import networkx as nx

from plasnet.base_graph import BaseGraph


class HubGraph(BaseGraph):
    """
    This is a class that recognises and labels hub plasmids.
    """

    def __init__(
        self,
        graph: Optional[nx.Graph] = None,
        hub_connectivity_threshold: int = 0,
        edge_density: float = 0.0,
        label: str = "",
    ):
        super().__init__(graph, label)
        self._hub_connectivity_threshold = hub_connectivity_threshold
        self._edge_density = edge_density

    def _get_node_shape(self, node: str) -> str:
        if node in self._get_hub_plasmids(use_cached=True):
            return "star"
        return "circle"

    def _add_special_node_attributes(self, node: str, attrs: dict[str, Any]) -> None:
        attrs["is_hub"] = node in self._get_hub_plasmids(use_cached=True)

    def _get_hub_plasmids(self, use_cached: bool = False) -> list[str]:
        need_to_compute_the_hub_plasmids = not use_cached or not hasattr(self, "_hub_plasmids")
        if need_to_compute_the_hub_plasmids:
            hub_plasmids_in_graph = []
            for node in self.nodes:
                if self.degree(node) >= self._hub_connectivity_threshold:
                    neighbors = list(self.neighbors(node))
                    subgraph = nx.induced_subgraph(self, neighbors)
                    nb_of_edges_between_neighbours = subgraph.number_of_edges()
                    max_nb_of_edges_between_neighbours = (
                        len(neighbors) * (len(neighbors) - 1)
                    ) // 2
                    edge_rate = nb_of_edges_between_neighbours / max_nb_of_edges_between_neighbours
                    if edge_rate <= self._edge_density:
                        hub_plasmids_in_graph.append(node)
                        logging.debug(f"{node} is a hub plasmid")
                    else:
                        logging.debug(
                            f"{node} is highly connected but does not connect "
                            f"unrelated plasmids, not a hub plasmid"
                        )
            self._hub_plasmids = hub_plasmids_in_graph

        return self._hub_plasmids

    def remove_hub_plasmids(self) -> None:
        while True:
            hub_plasmids = self._get_hub_plasmids()
            there_are_still_hub_plasmids = len(hub_plasmids) > 0
            if there_are_still_hub_plasmids:
                self.remove_nodes_from(hub_plasmids)
            else:
                break

    def _get_filters_HTML(self) -> str:
        nb_of_hubs = len(self._get_hub_plasmids(use_cached=True))
        return (
            f'<label for="hide_hubs">'
            f"Hide hub plasmids ({nb_of_hubs} present)"
            f"</label>"
            f'<input type="checkbox" id="hide_hubs" name="hide_hubs"><br/>'
        )

    def _get_custom_buttons_HTML(self) -> str:
        return '<div><input type="submit" value="Redraw" onclick="redraw()"></div>'

    @property
    def description(self) -> str:
        description = super().description
        hubs_detected = len(self._get_hub_plasmids(use_cached=True)) > 0
        if hubs_detected:
            description += " - WARNING: HUB PLASMID SPOTTED!"
        return description
