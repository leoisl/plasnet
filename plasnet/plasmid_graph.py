from pathlib import Path
from plasnet.communities import Communities
from plasnet.base_graph import BaseGraph
import networkx as nx


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
        # TODO: reads as pandas df, filter and load into networkx
        graph = PlasmidGraph()
        with open(distance_filepath) as distance_fh:
            next(distance_fh)  # skips header
            for line in distance_fh:
                from_plasmid, to_plasmid, distance = line.strip().split("\t")
                distance = float(distance)

                graph.add_node(from_plasmid)
                graph.add_node(to_plasmid)
                if distance <= distance_threshold:
                    graph.add_edge(from_plasmid, to_plasmid, weight=distance)

        return graph

    def split_graph_into_communities(self) -> Communities:
        return Communities(list(nx.connected_components(self)))
