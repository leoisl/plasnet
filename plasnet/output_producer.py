import collections
import logging
import shutil
from collections import defaultdict, namedtuple
from pathlib import Path

from plasnet.base_graph import BaseGraph
from plasnet.communities import Communities
from plasnet.list_of_graphs import ListOfGraphs
from plasnet.subcommunities import Subcommunities
from plasnet.Templates import Templates
from plasnet.utils import get_libs_dir


class OutputProducer:
    @staticmethod
    def produce_graph_visualisation(graph: BaseGraph, html_path: Path) -> None:
    def produce_graph_visualisation(graph: BaseGraph, html_path: Path):
        outdir = html_path.parent
        outdir.mkdir(exist_ok=True, parents=True)

        html = graph.produce_visualisation()
        html_path.write_text(html)

        OutputProducer.copy_libs(outdir)

    FileDescriptor = namedtuple("FileDescriptor", ["path", "description"])

    @staticmethod
    def produce_communities_visualisation(communities: Communities, outdir: Path) -> None:
        file_descriptors = OutputProducer._write_html_for_all_subgraphs(communities, outdir)
        OutputProducer._produce_index_file(outdir, communities, "Communities", file_descriptors)

    @staticmethod
    def produce_subcommunities_visualisation(subcommunities: Subcommunities, outdir: Path) -> None:
        file_descriptors = OutputProducer._write_html_for_all_subgraphs(subcommunities, outdir)
        OutputProducer._produce_index_file(outdir, subcommunities, "subcommunity", file_descriptors)

    @classmethod
    def _write_html_for_all_subgraphs(cls, subgraphs: ListOfGraphs, outdir: Path) -> list[FileDescriptor]:
        graphs_dir = outdir / "graphs"
        graphs_dir.mkdir(exist_ok=True, parents=True)
        file_descriptors = []

        for subgraph_index, subgraph in enumerate(subgraphs):
            html = subgraph.produce_visualisation()
            html_path = graphs_dir / f"{subgraph.label}.html"
            html_path.write_text(html)
            relative_html_path = f"graphs/{subgraph.label}.html"
            file_descriptors.append(cls.FileDescriptor(path=relative_html_path, description=subgraph.label))

        return file_descriptors

    @staticmethod
    def _produce_index_file(
        outdir: Path,
        graphs: ListOfGraphs,
        objects_description: str,
        file_descriptors: list[FileDescriptor],
        graph_to_sample_to_plasmids=None,
    ) -> None:
        nb_of_elems_to_graph_indexes = collections.defaultdict(list)
        if graph_to_sample_to_plasmids is None:
            # sort by edges
            for graph_index, graph in enumerate(graphs):
                nb_of_elems_to_graph_indexes[graph.number_of_edges()].append(graph_index)
        else:
            # sort by number of sample hits
            for graph_index, sample_to_plasmids in graph_to_sample_to_plasmids.items():
                nb_of_sample_hits = len(sample_to_plasmids)
                nb_of_elems_to_graph_indexes[nb_of_sample_hits].append(graph_index)

        index_src = Templates.read_template("index_template")

        visualisation_links = []
        for nb_of_elems in sorted(nb_of_elems_to_graph_indexes.keys(), reverse=True):
            for graph_index in nb_of_elems_to_graph_indexes[nb_of_elems]:
                graph = graphs[graph_index]
                file_descriptor = file_descriptors[graph_index]

                nb_of_blackhole_plasmids_for_graph = graph.get_nb_of_blackhole_plasmids()
                if nb_of_blackhole_plasmids_for_graph > 0:
                    warning = " - WARNING: BLACKHOLE SPOTTED!"
                else:
                    warning = ""
                description = f"View {file_descriptor.description}"
                if graph_to_sample_to_plasmids is not None:
                    description += f"- {len(graph_to_sample_to_plasmids[graph_index])} samples hit "
                description += f"({graph.number_of_edges()} edges, {graph.number_of_nodes()} nodes){warning}</a><br/>"
                visualisation_links.append(f'<a href="{file_descriptor.path}" target="_blank">{description}')

        with open(outdir / "index.html", "w") as index_fh:
            for line in index_src:
                if graph_to_sample_to_plasmids is None:
                    line = line.replace(
                        "<header_message>",
                        f"<h3>Largest {objects_description} are shown first</h3>",
                    )
                else:
                    line = line.replace(
                        "<header_message>",
                        f"<h3>{objects_description} with more sample hits are shown first</h3>",
                    )
                line = line.replace("<communities_links_tag>", "\n".join(visualisation_links))
                line = line.replace("<objects_description>", objects_description)
                print(line, file=index_fh)

        OutputProducer.copy_libs(outdir)

    @staticmethod
    def copy_libs(outdir: Path) -> None:
        shutil.copytree(get_libs_dir(), outdir / "libs", dirs_exist_ok=True)
