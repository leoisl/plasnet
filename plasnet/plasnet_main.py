from pathlib import Path
from plasnet.plasmid_graph import PlasmidGraph
import click
from plasnet.utils import PathlibPath, distance_df_to_dict
from plasnet.output_producer import OutputProducer
from plasnet.communities import Communities
import pandas as pd
import pickle
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


@click.group()
def cli():
    pass

@click.command(
    help="Creates and split a plasmid graph into communities",
    epilog="""
\b
Creates and split a plasmid graph into communities.
The plasmid graph is defined by plasmid and distance files.

\b
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

\b
The distances file is a tab-separated file with 3 columns: plasmid_1, plasmid_2, distance.
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
""")
@click.argument("plasmids", type=PathlibPath(exists=True))
@click.argument("distances", type=PathlibPath(exists=True))
@click.argument("output-dir", type=PathlibPath(exists=False))
@click.option("--distance-threshold", "-d", type=float, default=0.5, help="Distance threshold")
@click.option("--bh-connectivity", "-b", type=int, default=10, help="Minimum number of connections a plasmid need to be considered a blackhole plasmid")
@click.option("--bh-neighbours-edge-density", "-e", type=float, default=0.2, help="Maximum number of edge density between blackhole plasmid neighbours to label the plasmid as blackhole")
@click.option("--output-plasmid-graph", "-p", is_flag=True, help="Also outputs the full, unsplit, plasmid graph")
def split(plasmids: Path,
          distances: Path,
          output_dir: Path,
          distance_threshold: float,
          bh_connectivity: int,
          bh_neighbours_edge_density: float,
          output_plasmid_graph: bool):
    visualisations_dir = output_dir/"visualisations"
    logging.info(f"Creating plasmid graph from {plasmids} and {distances}")
    plasmid_graph = PlasmidGraph.build(plasmids, distances, distance_threshold)

    if output_plasmid_graph:
        logging.info(f"Producing full plasmid graph visualisation")
        OutputProducer.produce_graph_visualisation(plasmid_graph, visualisations_dir/"single_graph"/"single_graph.html")

    logging.info(f"Splitting plasmid graph into communities")
    communities = plasmid_graph.split_graph_into_communities(bh_connectivity, bh_neighbours_edge_density)

    logging.info(f"Producing communities visualisation")
    OutputProducer.produce_communities_visualisation(communities, visualisations_dir/"communities")

    logging.info(f"Serialising objects")
    objects_dir = output_dir/"objects"
    objects_dir.mkdir(parents=True, exist_ok=True)
    plasmid_graph.save(objects_dir/"plasmid_graph.pkl")
    communities.save(objects_dir/"communities.pkl")
    communities.save_graph_as_text(objects_dir/"communities.txt")

    logging.info(f"All done!")


@click.command(
    help="Type the communities of a previously split plasmid graph into subcommunities or types",
    epilog="""
\b
Type the communities of a previously split plasmid graph into subcommunities or types.
This typing is based on running an asynchronous label propagation algorithm on the previously identified communities.
This algorithm is implemented in the networkx library, and relies on a given distance file.
This distance file should be a more precise and careful distance function than the one used to split the graph into communities.
For example, you could use gene jaccard distance to split the graph and the DCJ-indel distance to type the communities.
See https://github.com/iqbal-lab-org/pling for a tool to compute gene jaccard and DCJ-indel distances. 

\b
The first file, describing the communities, is a pickle file (.pkl) that can be found in <split_out_dir>/objects/communities.pkl,
where <split_out_dir> is the output dir of the split command.

\b
The distances file is a tab-separated file with 3 columns: plasmid_1, plasmid_2, distance.
plasmid_1 and plasmid_2 are plasmid names, and distance is a float number.
The distance threshold is the minimum distance value for two plasmids to be considered connected.
Example of such file:
plasmid_1       plasmid_2       distance
AP024796.1      AP024825.1      4
AP024796.1      CP012142.1      10
AP024796.1      CP014494.1      20
AP024796.1      CP019149.1      1
AP024796.1      CP021465.1      0
AP024796.1      CP022675.1      50
AP024796.1      CP024687.1      1000
AP024796.1      CP026642.1      20
AP024796.1      CP027485.1      1
""")
@click.argument("communities-pickle", type=PathlibPath(exists=True))
@click.argument("distances", type=PathlibPath(exists=True))
@click.argument("output-dir", type=PathlibPath(exists=False))
@click.option("--distance-threshold", "-d", type=float, default=4, help="Distance threshold")
@click.option('--small-subcommunity-size-threshold', type=int, default=4,
              help='Subcommunities with size up to this parameter will be joined to neighbouring larger subcommunities')
def type( communities_pickle: Path,
          distances: Path,
          output_dir: Path,
          distance_threshold: float,
          small_subcommunity_size_threshold: int):
    logging.info(f"Loading communities from {communities_pickle}")
    communities: Communities = Communities.load(communities_pickle)

    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"Loading distances from {distances}")
    distance_df = pd.read_csv(distances, sep="\t")
    distance_dict = distance_df_to_dict(distance_df)

    logging.info(f"Filtering communities by distance")
    communities.filter_by_distance(distance_dict, distance_threshold)

    logging.info(f"Typing communities (i.e. splitting them into subcommunities)")
    all_subcommunities = []
    for community in communities:
        community.remove_blackhole_plasmids()
        subcommunities = community.split_graph_into_subcommunities(small_subcommunity_size_threshold)
        all_subcommunities.append(subcommunities)

    logging.info("Producing communities visualisations")
    OutputProducer.produce_communities_visualisation(communities, output_dir / "visualisations/communities")

    logging.info("Producing subcommunities visualisations")
    OutputProducer.produce_subcommunities_visualisation(all_subcommunities, output_dir/"visualisations/subcommunities")

    logging.info("Serialising objects")
    objects_dir = output_dir / "objects"
    objects_dir.mkdir(parents=True, exist_ok=True)
    communities.save(objects_dir / "communities.pkl")
    with open(objects_dir / "subcommunities.pkl", "wb") as all_subcommunities_fh:
        pickle.dump(all_subcommunities, all_subcommunities_fh)

    logging.info("All done!")


# Add commands to the main group
cli.add_command(split)
cli.add_command(type)


def main():
    """Entry point for the application script"""
    cli()
