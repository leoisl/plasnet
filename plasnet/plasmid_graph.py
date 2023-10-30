from pathlib import Path
from communities import Communities
from base_graph import BaseGraph
from community_graph import CommunityGraph
import networkx as nx
import pandas as pd


class PlasmidGraph(BaseGraph):
    """
    Class to represent a plasmid graph.
    It represents a full plasmid graph, not partitioned into communities or subcommunities.
    Each node is a plasmid, and each edge represents an abstract distance between two plasmids.
    """

    @staticmethod
    def from_distance_file(distance_filepath: Path, distance_threshold: float) -> "PlasmidGraph":
        """
        Creates a plasmid graph from a plasmid distance file.
        The distance file is a tab-separated file with 3 columns: plasmid_1, plasmid_2, distance.
        plasmid_1 and plasmid_2 are plasmid names, and distance is a float between 0 and 1.
        The distance threshold is the minimum distance value for two plasmids to be considered connected.

        Example of such file:
        plasmid_1       plasmid_2       distance
        AP024796.1      AP024825.1      0.8
        AP024796.1      CP012142.1      0.5
        AP024796.1      CP014494.1      0.3
        AP024796.1      CP019149.1      0.0
        AP024796.1      CP021465.1      0.0
        AP024796.1      CP022675.1      1.0
        AP024796.1      CP024687.1      0.0
        AP024796.1      CP026642.1      0.5
        AP024796.1      CP027485.1      0.8
        """
        df = pd.read_csv(distance_filepath, sep="\t")

        # apply distance threshold
        df = df[df["distance"] <= distance_threshold]

        # create graph
        graph = nx.from_pandas_edgelist(df, source="plasmid_1", target="plasmid_2", edge_attr="distance",
                                        create_using=PlasmidGraph)

        return graph

    def split_graph_into_communities(self, bh_connectivity: int, bh_neighbours_edge_density: float) -> Communities:
        return Communities(
            CommunityGraph(self.subgraph(component), bh_connectivity, bh_neighbours_edge_density)
            for component in nx.connected_components(self))

    def _get_libs_relative_path(self) -> str:
        return "."

    def _get_samples_selectors_HTML(self) -> str:
        return ""

    def _get_filters_HTML(self) -> str:
        return ""

    def _get_custom_buttons_HTML(self) -> str:
        return ""
