import logging
from copy import deepcopy
from pathlib import Path
from typing import Optional, cast

import click
import pandas as pd

from plasnet import __version__
from plasnet.communities import Communities
from plasnet.output_producer import OutputProducer
from plasnet.plasmid_graph import PlasmidGraph
from plasnet.sample_graph import SampleGraph
from plasnet.sample_graphs import SampleGraphs
from plasnet.subcommunities import Subcommunities
from plasnet.utils import PathlibPath, distance_df_to_dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
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
""",  # noqa: E501
)
@click.argument("plasmids", type=PathlibPath(exists=True))
@click.argument("distances", type=PathlibPath(exists=True))
@click.argument("output-dir", type=PathlibPath(exists=False))
@click.option("--distance-threshold", "-d", type=float, default=0.5, help="Distance threshold")
@click.option(
    "--bh-connectivity",
    "-b",
    type=int,
    default=10,
    help="Minimum number of connections a plasmid need to be considered a hub plasmid",
)
@click.option(
    "--bh-neighbours-edge-density",
    "-e",
    type=float,
    default=0.2,
    help="Maximum number of edge density between hub plasmid neighbours to "
    "label the plasmid as hub",
)
@click.option(
    "--output-plasmid-graph",
    "-p",
    is_flag=True,
    help="Also outputs the full, unsplit, plasmid graph",
)
@click.option(
    "--output-type",
    type=str,
    default="html",
    help="Whether to output networks as html visualisations, cytoscape formatted json, or both."
)
@click.option(
    "--plasmids-metadata", type=PathlibPath(exists=True), help="Plasmids metadata text file."
)
def split(
    plasmids: Path,
    distances: Path,
    output_dir: Path,
    distance_threshold: float,
    bh_connectivity: int,
    bh_neighbours_edge_density: float,
    output_plasmid_graph: bool,
    output_type: Optional[str],
    plasmids_metadata: Optional[Path],
) -> None:
    visualisations_dir = output_dir / "visualisations"
    logging.info(f"Creating plasmid graph from {plasmids} and {distances}")
    metadata = []
    if plasmids_metadata:
        metadata = plasmids_metadata.read_text().splitlines()
    plasmid_graph = PlasmidGraph.build(plasmids, distances, distance_threshold, metadata)

    if output_plasmid_graph:
        logging.info("Producing full plasmid graph visualisation")
        OutputProducer.produce_graph_visualisation(
            plasmid_graph, visualisations_dir / "single_graph" / "single_graph.html"
        )

    logging.info("Splitting plasmid graph into communities")
    communities = plasmid_graph.split_graph_into_communities(
        bh_connectivity, bh_neighbours_edge_density
    )

    logging.info("Producing communities visualisation")
    OutputProducer.produce_communities_visualisation(
        communities, visualisations_dir / "communities", output_type
    )

    logging.info("Serialising objects")
    objects_dir = output_dir / "objects"
    objects_dir.mkdir(parents=True, exist_ok=True)
    plasmid_graph.save(objects_dir / "plasmid_graph.pkl")
    communities.save(objects_dir / "communities.pkl")
    communities.save_graph_as_text(objects_dir / "communities.txt")
    communities.save_classification(objects_dir / "communities.tsv", "plasmid\tcommunity")

    logging.info("All done!")


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
""",  # noqa: E501
)
@click.argument("communities-pickle", type=PathlibPath(exists=True))
@click.argument("distances", type=PathlibPath(exists=True))
@click.argument("output-dir", type=PathlibPath(exists=False))
@click.option("--distance-threshold", "-d", type=float, default=4, help="Distance threshold")
@click.option(
    "--small-subcommunity-size-threshold",
    type=int,
    default=4,
    help="Subcommunities with size up to this parameter will be joined to "
    "neighbouring larger subcommunities",
)
@click.option(
    "--output-type",
    type=str,
    default="html",
    help="Whether to output networks as html visualisations, cytoscape formatted json, or both."
)
def type(
    communities_pickle: Path,
    distances: Path,
    output_dir: Path,
    distance_threshold: float,
    small_subcommunity_size_threshold: int,
    output_type: Optional[str],
) -> None:
    logging.info(f"Loading communities from {communities_pickle}")
    communities = cast(Communities, Communities.load(communities_pickle))

    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"Loading typing distances from {distances}")
    distance_df = pd.read_csv(distances, sep="\t")
    distance_dict = distance_df_to_dict(distance_df)

    logging.info("Adding typing distance in plasmid graph")
    communities.add_typing_distances(distance_dict)

    logging.info("Backing up communities before applying distance filter")
    original_communities = deepcopy(communities)

    logging.info("Applying distance filter")
    communities.filter_by_distance(distance_threshold)

    logging.info("Typing communities (i.e. splitting them into subcommunities)")
    all_subcommunities = Subcommunities()
    all_hub_plasmids = set()
    for community in communities:
        hub_plasmids = community.remove_hub_plasmids()
        all_hub_plasmids.update(hub_plasmids)
        subcommunities = community.split_graph_into_subcommunities(
            small_subcommunity_size_threshold
        )
        all_subcommunities.extend(subcommunities)

    logging.info("Producing communities visualisations")
    original_communities.recolour_nodes(communities)
    OutputProducer.produce_communities_visualisation(
        original_communities, output_dir / "visualisations/communities", output_type
    )

    logging.info("Producing subcommunities visualisations")
    OutputProducer.produce_subcommunities_visualisation(
        all_subcommunities, output_dir / "visualisations/subcommunities", output_type
    )

    logging.info("Serialising objects")
    objects_dir = output_dir / "objects"
    objects_dir.mkdir(parents=True, exist_ok=True)
    original_communities.save(objects_dir / "communities.pkl")
    all_subcommunities.save(objects_dir / "subcommunities.pkl")
    all_subcommunities.save_classification(objects_dir / "typing.tsv", "plasmid\ttype")
    with open(objects_dir / "hub_plasmids.csv", "w") as hub_plasmids_fh:
        print("hub_plasmids", file=hub_plasmids_fh)
        for plasmid in all_hub_plasmids:
            print(plasmid, file=hub_plasmids_fh)

    logging.info("All done!")


@click.command(
    help="Add sample hits annotations on top of previously identified subcommunities or types",
    epilog="""
\b
Add sample hits annotations on top of previously identified subcommunities or types.


\b
The first file, describing the subcommunities, is a pickle file (.pkl) that can be found in <type_out_dir>/objects/subcommunities.pkl,
where <type_out_dir> is the output dir of the type command.

\b
The sample-hits file is a tab-separated file with 2 columns: sample, plasmid.
These columns are self-explanatory and identifies the plasmids present in each sample.
Example of such file:
sample              plasmid
cpe001_trim_ill     NZ_CP006799.1
cpe001_trim_ill     NZ_CP028929.1
cpe002_trim_ill     NZ_CP079159.1
cpe005_trim_ill     NZ_CP006799.1
cpe005_trim_ill     NZ_CP079676.1
cpe010_trim_ill     NZ_CP028929.1
cpe020_trim_ill     NZ_CP006799.1
cpe020_trim_ill     NZ_CP079676.1
cpe021_trim_ill     NZ_CP006799.1
""",  # noqa: E501
)
@click.argument("subcommunities-pickle", type=PathlibPath(exists=True))
@click.argument("sample-hits", type=PathlibPath(exists=True))
@click.argument("output-dir", type=PathlibPath(exists=False))
@click.option(
    "--output-type",
    type=str,
    default="html",
    help="Whether to output networks as html visualisations, cytoscape formatted json, or both."
)
def add_sample_hits(
    subcommunities_pickle: Path,
    sample_hits: Path,
    output_dir: Path,
) -> None:
    logging.info(f"Loading subcommunities from {subcommunities_pickle}")
    subcommunities = cast(Subcommunities, Subcommunities.load(subcommunities_pickle))

    logging.info(f"Loading sample hits from {sample_hits}")
    sample_hits_df = pd.read_csv(sample_hits, sep="\t")

    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Producing sample graphs")
    sample_graphs = SampleGraphs()
    for subcommunity in subcommunities:
        sample_plasmid_for_this_subcommunity = sample_hits_df[
            sample_hits_df["plasmid"].isin(subcommunity.nodes)
        ]
        sample_graph = SampleGraph.from_subcommunity_graph(
            subcommunity, sample_plasmid_for_this_subcommunity
        )
        sample_graphs.append(sample_graph)

    logging.info("Producing sample graphs visualisations")
    OutputProducer.produce_subcommunities_visualisation(
        sample_graphs, output_dir / "visualisations/sample_graphs", output_type
    )

    logging.info("All done!")


# Add commands to the main group
cli.add_command(split)
cli.add_command(type)
cli.add_command(add_sample_hits)


def main() -> None:
    """Entry point for the application script"""
    cli()
