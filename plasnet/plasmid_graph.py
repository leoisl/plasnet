from pathlib import Path
from plasnet.communities import Communities
from plasnet.base_graph import BaseGraph
import networkx as nx


class PlasmidGraph(BaseGraph):
    """
    Class to represent a plasmid graph.
    It represents a full plasmid graph, not partitioned into communities or subcommunities.
    Each node is a plasmid, and each edge represents the gene jaccard similarity between two plasmids.
    """

    @staticmethod
    def from_gene_jaccard_file(gene_jaccard_filepath: Path, gene_jaccard_threshold: float) -> "PlasmidGraph":
        """
        Creates a plasmid graph from a gene jaccard similarity file.
        The gene jacard file is a tab-separated file with 3 columns: plasmid_1, plasmid_2, gene_jaccard, for example:
        plasmid_1       plasmid_2       gene_jaccard
        AP024796.1      AP024825.1      0.0
        AP024796.1      CP012142.1      0.007575757575757576
        AP024796.1      CP014494.1      0.010309278350515464
        AP024796.1      CP019149.1      0.0
        AP024796.1      CP021465.1      0.0
        AP024796.1      CP022675.1      0.0
        AP024796.1      CP024687.1      0.0
        AP024796.1      CP026642.1      0.07575757575757576
        AP024796.1      CP027485.1      0.09848484848484848

        The definition of gene jaccard between two plasmids is the number of common genes divided by the number of genes.
        The gene jaccard threshold is the minimum gene jaccard value for two plasmids to be considered connected.
        """
        graph = PlasmidGraph()
        with open(gene_jaccard_filepath) as gene_jaccard_fh:
            next(gene_jaccard_fh)  # skips header
            for line in gene_jaccard_fh:
                from_plasmid, to_plasmid, gene_jaccard = line.strip().split("\t")
                gene_jaccard = float(gene_jaccard)

                graph.add_node(from_plasmid)
                graph.add_node(to_plasmid)
                if gene_jaccard >= gene_jaccard_threshold:
                    graph.add_edge(from_plasmid, to_plasmid, weight=gene_jaccard)

        return graph

    def split_graph_into_communities(self) -> Communities:
        return Communities(list(nx.connected_components(self)))
