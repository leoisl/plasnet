from pathlib import Path
from plasnet.plasmid_graph import PlasmidGraph
import click


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
@click.argument("distances", type=click.Path(exists=True))
@click.argument("output-dir", type=click.Path(exists=False))
@click.option("--distance-threshold", "-t", type=float, default=0.5, help="Distance threshold")
@click.option("--output-plasmid-graph", "-p", is_flag=True, help="Also outputs the full, unsplit, plasmid graph")
def split(distances: Path,
          output_dir: Path,
          distance_threshold: float,
          output_plasmid_graph: bool):
    plasmid_graph = PlasmidGraph.from_distance_file(distances, distance_threshold)

    if output_plasmid_graph:
        plasmid_graph.produce_visualisation(output_dir/"plasmid_graph", "plasmid_graph", 0, False, False)

    communities = plasmid_graph.split_graph_into_communities()
    for community in communities:
        community.produce_visualisation(output_dir/"communities", "community", 0, False, False)


def main():
    """Entry point for the application script"""
    split()
