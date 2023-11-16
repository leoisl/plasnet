from pathlib import Path
from typing import Optional

import networkx as nx
import pandas as pd

from plasnet.base_graph import BaseGraph
from plasnet.communities import Communities
from plasnet.community_graph import CommunityGraph
from plasnet.utils import DistanceTags


class PlasmidGraph(BaseGraph):
    """
    Class to represent a plasmid graph.
    It represents a full plasmid graph, not partitioned into communities or subcommunities.
    Each node is a plasmid, and each edge represents an abstract distance between two plasmids.
    """

    def __init__(self, graph: Optional[nx.Graph] = None, label: str = "") -> None:
        super().__init__(graph, label)

    @staticmethod
    def build(
        plasmids_filepath: Path, distance_filepath: Path, distance_threshold: float
    ) -> "PlasmidGraph":
        """
        Creates a plasmid graph from plasmid and distance files.

        The plasmid file is a tab-separated file with one column describing all plasmids in the dataset.
        Example of such file:
        plasmid
        AP024796.1
        AP024825.1
        CP012142.1
        CP014494.1
        CP019149.1
        CP021465.1
        CP022675.1
        CP024687.1
        CP026642.1
        CP027485.1

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
        """  # noqa: E501
        plasmids = pd.read_csv(plasmids_filepath)

        distance_df = pd.read_csv(distance_filepath, sep="\t")
        distance_df[DistanceTags.SplitDistanceTag.value] = distance_df["distance"]

        # apply distance threshold
        distance_df = distance_df[
            distance_df[DistanceTags.SplitDistanceTag.value] <= distance_threshold
        ]

        # round distance to 2 decimals
        distance_df[DistanceTags.SplitDistanceTag.value] = distance_df[
            DistanceTags.SplitDistanceTag.value
        ].round(2)

        # create graph
        graph = nx.from_pandas_edgelist(
            distance_df,
            source="plasmid_1",
            target="plasmid_2",
            edge_attr=DistanceTags.SplitDistanceTag.value,
            create_using=PlasmidGraph,
        )
        graph.add_nodes_from(plasmids["plasmid"])

        return PlasmidGraph(graph)

    def split_graph_into_communities(
        self, bh_connectivity: int, bh_neighbours_edge_density: float
    ) -> Communities:
        return Communities(
            CommunityGraph(
                self.subgraph(component),
                bh_connectivity,
                bh_neighbours_edge_density,
                label=f"community_{idx}",
            )
            for idx, component in enumerate(nx.connected_components(self))
        )

    def _get_libs_relative_path(self) -> str:
        return "."

    def _get_samples_selectors_HTML(self) -> str:
        return ""

    def _get_filters_HTML(self) -> str:
        return ""

    def _get_custom_buttons_HTML(self) -> str:
        return ""
