# TODO: refactor

from typing import Optional

from plasnet.alt_label_propagation import appendable_lpa_communities

import networkx as nx

from plasnet.ColorPicker import ColorPicker
from plasnet.hub_graph import HubGraph
from plasnet.subcommunities import Subcommunities
from plasnet.subcommunity_graph import SubcommunityGraph
from plasnet.utils import DistanceDict, DistanceTags


class CommunityGraph(HubGraph):
    def __init__(
        self,
        graph: Optional[nx.Graph] = None,
        hub_connectivity_threshold: int = 0,
        edge_density: float = 0.0,
        label: str = "",
    ):
        super().__init__(graph, hub_connectivity_threshold, edge_density, label)
        self._node_to_colour: dict[str, str] = {}

    def _get_node_color(self, node: str) -> str:
        return self._node_to_colour.get(node, ColorPicker.get_default_color())

    @staticmethod
    def _get_node_to_subcommunity(subcommunities: list[set[str]]) -> dict[str, int]:
        node_to_subcommunity = {}
        for subcommunity_index, subcommunity in enumerate(subcommunities):
            for node in subcommunity:
                node_to_subcommunity[node] = subcommunity_index
        return node_to_subcommunity

    def _fix_small_subcommunities(
        self, subcommunities: list[set[str]], small_subcommunity_size_threshold: int
    ) -> list[set[str]]:
        # sort subcommunities by size so that we can safely move
        # smaller subcommunities into larger ones
        subcommunities = sorted(subcommunities, key=lambda subcommunity: len(subcommunity))
        node_to_subcommunity = self._get_node_to_subcommunity(subcommunities)

        for subcommunity_idx, subcommunity in enumerate(subcommunities):
            subcommunity_is_too_small = len(subcommunity) <= small_subcommunity_size_threshold
            if subcommunity_is_too_small:
                subcommunity_neighbours = set(
                    neighbor for node in subcommunity for neighbor in self.neighbors(node)
                ) - set(subcommunity)
                subcommunity_has_no_neighbors = len(subcommunity_neighbours) == 0
                if subcommunity_has_no_neighbors:
                    continue

                candidate_subcommunities = set(
                    node_to_subcommunity[neighbor] for neighbor in subcommunity_neighbours
                )
                largest_subcommunity_size = max(
                    len(subcommunities[subcommunity]) for subcommunity in candidate_subcommunities
                )
                small_will_be_integrated_into_large = largest_subcommunity_size >= len(subcommunity)
                if small_will_be_integrated_into_large:
                    largest_subcommunity_idx = next(
                        filter(
                            lambda idx: len(subcommunities[idx]) == largest_subcommunity_size,
                            candidate_subcommunities,
                        )
                    )
                    subcommunities[largest_subcommunity_idx].update(subcommunity)
                    subcommunities[subcommunity_idx] = set()
        return subcommunities

    def split_graph_into_subcommunities(
        self, small_subcommunity_size_threshold: int
    ) -> Subcommunities:
        subcommunities_nodes: list[set[str]] = list(
            nx.community.asyn_lpa_communities(G=self, seed=42)
        )
        subcommunities_nodes = self._fix_small_subcommunities(
            subcommunities_nodes, small_subcommunity_size_threshold
        )

        subcommunities = []
        for subcommunity_index, subcommunity_nodes in enumerate(subcommunities_nodes):
            colour = ColorPicker.get_color_given_index(subcommunity_index)

            subcommunity = SubcommunityGraph(
                self.subgraph(subcommunity_nodes),
                self._hub_connectivity_threshold,
                self._edge_density,
                label=f"{self.label}_subcommunity_{subcommunity_index}",
                colour=colour,
            )
            subcommunities.append(subcommunity)

            for node in subcommunity_nodes:
                self._node_to_colour[node] = colour

        return Subcommunities(subcommunities)
    
    def split_graph_given_labels(
            self, small_subcommunity_size_threshold: int, typing: dict
    ) -> Subcommunities:
        if typing:
            map = {typing[n]: i for i,n in enumerate(typing.keys())}
            initial_labels = {n: map[typing[n]] for n in self if n in typing.keys()}
        subcommunities_nodes: list[set[str]] = list(
            appendable_lpa_communities(G=self, initial_labels=initial_labels, seed=42)
        )
        subcommunities_nodes = self._fix_small_subcommunities(
            subcommunities_nodes, small_subcommunity_size_threshold
        )

        subcommunities = []
        for subcommunity_index, subcommunity_nodes in enumerate(subcommunities_nodes):
            colour = ColorPicker.get_color_given_index(subcommunity_index)

            subcommunity = SubcommunityGraph(
                self.subgraph(subcommunity_nodes),
                self._hub_connectivity_threshold,
                self._edge_density,
                label=f"{self.label}_subcommunity_{subcommunity_index}",
                colour=colour,
            )
            subcommunities.append(subcommunity)

            for node in subcommunity_nodes:
                self._node_to_colour[node] = colour

        return Subcommunities(subcommunities)
    
    def nearest_neighbour(
        self, typing, new_plasmids
    ) -> Subcommunities:
        subcommunity_names = set(typing["type"].to_list()) 
        subcommunity_labels = {subcomm:[plasmid for plasmid in typing[typing["type"]==subcomm]["plasmid"].values] for subcomm in list(subcommunity_names) if subcomm.split("_")[1]==self.label.split("_")[1]} #select only those that are in this community
        max_label = len(subcommunity_labels.keys())
        
        for plasmid in new_plasmids:
            if plasmid in self.graph:
                neighbours = [n for n in self.graph[plasmid]]
                if len(neighbours)==0:
                    subcommunity_labels[f"community_{self.label}_subcommunity_{max_label}"] = [plasmid]
                    max_label = max_label + 1
                else:
                    neighbours = sorted(neighbours, key=lambda n: self.graph[n,plasmid][DistanceTags.SplitDistanceTag.value])
                    min_dist = self.graph[neighbours[0],plasmid][DistanceTags.SplitDistanceTag.value]
                    nearest = [neighbour for neighbour in neighbours if self.graph[neighbour,plasmid][DistanceTags.SplitDistanceTag.value]==min_dist]
                    nearest = sorted(nearest, key=lambda n: len(typing[typing["type"]==typing[typing["plasmid"]==n]["type"].values[0]]))
                    nn = nearest[-1] #select nearest neighbour with largest subcommunity size
                    subcommunity_labels[typing[typing["plasmid"]==nn]["type"].values[0]].append(nn)
                

        subcommunities = []
        for subcommunity_label in subcommunity_labels.keys():
            subcommunity_index = int(subcommunity_label.split("_")[-1])
            colour = ColorPicker.get_color_given_index(subcommunity_index)

            subcommunity = SubcommunityGraph(
                self.subgraph(subcommunity_labels[subcommunity_label]),
                self._hub_connectivity_threshold,
                self._edge_density,
                label=subcommunity_label, #reuse old labels here!
                colour=colour,
            )
            subcommunities.append(subcommunity)

            for node in subcommunity_labels[subcommunity_label]:
                self._node_to_colour[node] = colour

        return Subcommunities(subcommunities)

    def _get_libs_relative_path(self) -> str:
        return ".."

    def _get_samples_selectors_HTML(self) -> str:
        return ""

    def add_typing_distances(self, distance_dict: DistanceDict) -> None:
        for edge in self.edges:
            self.edges[edge][DistanceTags.TypeDistanceTag.value] = distance_dict.get(
                edge, float("inf")
            )

    def filter_by_distance(self, distance_threshold: float) -> None:
        edges_to_remove = []
        for edge in self.edges:
            edge_should_be_removed = (
                self.edges[edge][DistanceTags.TypeDistanceTag.value] > distance_threshold
            )
            if edge_should_be_removed:
                edges_to_remove.append(edge)

        self.remove_edges_from(edges_to_remove)

    def recolour_nodes(self, other_community: "CommunityGraph") -> None:
        for node in self.nodes:
            self._node_to_colour[node] = other_community._get_node_color(node)
