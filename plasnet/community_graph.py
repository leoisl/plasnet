# TODO: refactor

from plasnet.base_graph import BaseGraph
from plasnet.subcommunities import Subcommunities
from plasnet.subcommunity_graph import SubcommunityGraph
import networkx as nx
import logging
from typing import List, Dict


class CommunityGraph(BaseGraph):
    def get_blackhole_plasmids(self, blackhole_connectivity_threshold: int, edge_density: float) -> List["Nodes"]:
        blackhole_plasmids_in_graph = []
        for node in self.nodes:
            if self.degree(node) >= blackhole_connectivity_threshold:
                neighbors = list(self.neighbors(node))
                subgraph = nx.induced_subgraph(self, neighbors)
                nb_of_edges_between_neighbours = subgraph.number_of_edges()
                max_nb_of_edges_between_neighbours = (len(neighbors) * (len(neighbors) - 1)) // 2
                edge_rate = nb_of_edges_between_neighbours / max_nb_of_edges_between_neighbours
                if edge_rate <= edge_density:
                    blackhole_plasmids_in_graph.append(node)
                    logging.debug(f"{node} is a blackhole plasmid, REMOVED")
                else:
                    logging.debug(f"{node} is highly connected but does not connect unrelated plasmids, not removed")
        return blackhole_plasmids_in_graph

    def remove_plasmids(self, plasmids_to_be_removed: List["Nodes"]):
        self.remove_nodes_from(plasmids_to_be_removed)

    @staticmethod
    def _get_node_to_subcommunity(subcommunities):
        node_to_subcommunity = {}
        for subcommunity_index, subcommunity in enumerate(subcommunities):
            for node in subcommunity:
                node_to_subcommunity[node] = subcommunity_index
        return node_to_subcommunity

    def _fix_small_subcommunities(self, subcommunities, small_subcommunity_size_threshold) -> List[SubcommunityGraph]:
        # sort subcommunities by size so that we can safely move smaller subcommunities into larger ones
        subcommunities = sorted(subcommunities, key=lambda subcommunity: len(subcommunity))
        node_to_subcommunity = self._get_node_to_subcommunity(subcommunities)

        for subcommunity_idx, subcommunity in enumerate(subcommunities):
            subcommunity_is_too_small = len(subcommunity) <= small_subcommunity_size_threshold
            if subcommunity_is_too_small:
                subcommunity_neighbours = set(
                    neighbor for node in subcommunity for neighbor in self.neighbors(node)) - set(subcommunity)
                subcommunity_has_no_neighbors = len(subcommunity_neighbours) == 0
                if subcommunity_has_no_neighbors:
                    continue

                candidate_subcommunities = set(node_to_subcommunity[neighbor] for neighbor in subcommunity_neighbours)
                largest_subcommunity_size = max(
                    len(subcommunities[subcommunity]) for subcommunity in candidate_subcommunities)
                small_will_be_integrated_into_large = largest_subcommunity_size >= len(subcommunity)
                if small_will_be_integrated_into_large:
                    largest_subcommunity_idx = next(
                        filter(lambda idx: len(subcommunities[idx]) == largest_subcommunity_size,
                               candidate_subcommunities))
                    subcommunities[largest_subcommunity_idx].update(subcommunity)
                    subcommunities[subcommunity_idx] = set()
        return subcommunities


    def split_graph_into_subcommunities(self, plasmid_to_plasmid_to_dcj_dist: Dict[str, Dict[str, int]], dcj_dist_threshold: int, small_subcommunity_size_threshold) -> Subcommunities:
        local_subcommunities = list(nx.community.asyn_lpa_communities(G=self, weight='weight', seed=42))
        local_subcommunities = self._fix_small_subcommunities(local_subcommunities, small_subcommunity_size_threshold=small_subcommunity_size_threshold)
        return Subcommunities(local_subcommunities)
