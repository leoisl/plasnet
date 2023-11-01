from pathlib import Path
from plasnet.plasmid_graph import PlasmidGraph
import click
from plasnet.utils import PathlibPath
from plasnet.output_producer import OutputProducer


@click.command(epilog="""
\b
Creates and split a plasmid graph into communities.
The plasmid graph is defined by a plasmid distances file.
The distances file is a tab-separated file with 3 columns: plasmid_1, plasmid_2, distance.
plasmid_1 and plasmid_2 are plasmid names, and distance is a float between 0 and 1.
The distance threshold is the minimum distance value for two plasmids to be considered connected.

\b
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
""")
@click.argument("distances", type=PathlibPath(exists=True))
@click.argument("output-dir", type=PathlibPath(exists=False))
@click.option("--distance-threshold", "-d", type=float, default=0.5, help="Distance threshold")
@click.option("--bh-connectivity", "-b", type=int, default=10, help="Minimum number of connections a plasmid need to be considered a blackhole plasmid")
@click.option("--bh-neighbours-edge-density", "-e", type=float, default=0.2, help="Maximum number of edge density between blackhole plasmid neighbours to label the plasmid as blackhole")
@click.option("--output-plasmid-graph", "-p", is_flag=True, help="Also outputs the full, unsplit, plasmid graph")
def split(distances: Path,
          output_dir: Path,
          distance_threshold: float,
          bh_connectivity: int,
          bh_neighbours_edge_density: float,
          output_plasmid_graph: bool):
    visualisations_dir = output_dir/"visualisations"
    plasmid_graph = PlasmidGraph.build(plasmids, distances, distance_threshold)

    if output_plasmid_graph:
        OutputProducer.produce_graph_visualisation(plasmid_graph, visualisations_dir/"single_graph"/"single_graph.html")

    communities = plasmid_graph.split_graph_into_communities(bh_connectivity, bh_neighbours_edge_density)
    OutputProducer.produce_communities_visualisation(communities, visualisations_dir/"communities")

    objects_dir = output_dir/"objects"
    objects_dir.mkdir(parents=True, exist_ok=True)
    plasmid_graph.save(objects_dir/"plasmid_graph.pkl")
    communities.save(objects_dir/"communities.pkl")

    communities.save_graph_as_text(objects_dir/"communities.txt")

def main():
    """Entry point for the application script"""
    split()
