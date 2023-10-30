import collections
import shutil
from Templates import Templates
from utils import get_libs_dir
import logging
from collections import defaultdict
from base_graph import BaseGraph
from pathlib import Path


class OutputProducer:
    @staticmethod
    def produce_index_file(outdir, graphs, graphs_descriptions, objects_description, blackhole_plasmids, graph_to_sample_to_plasmids=None):
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
        visualisation_links=[]
        for nb_of_elems in sorted(nb_of_elems_to_graph_indexes.keys(), reverse=True):
            for graph_index in nb_of_elems_to_graph_indexes[nb_of_elems]:
                graph = graphs[graph_index]
                blackhole_plasmids_for_graph = blackhole_plasmids[graph_index]
                if len(blackhole_plasmids_for_graph)>0:
                    warning=" - WARNING: BLACKHOLE SPOTTED!"
                else:
                    warning=""
                description = f'View {objects_description} {graphs_descriptions[graph_index]} '
                if graph_to_sample_to_plasmids is not None:
                    description += f"- {len(graph_to_sample_to_plasmids[graph_index])} samples hit "
                description += f'({graph.number_of_edges()} edges, {graph.number_of_nodes()} nodes){warning}</a><br/>'
                visualisation_links.append(f'<a href="graphs/{graphs_descriptions[graph_index]}.html" target="_blank">{description}')

        with open(outdir / f"index.html", "w") as index_fh:
            for line in index_src:
                if graph_to_sample_to_plasmids is None:
                    line = line.replace("<header_message>", f"<h3>Largest {objects_description} are shown first</h3>")
                else:
                    line = line.replace("<header_message>", f"<h3>{objects_description} with more sample hits are shown first</h3>")
                line = line.replace("<communities_links_tag>", "\n".join(visualisation_links))
                line = line.replace("<objects_description>", objects_description)
                print(line, file=index_fh)

        OutputProducer.copy_libs(outdir)

    @staticmethod
    def produce_full_visualization(graphs, plasmid_to_subcommunity, visualisation_outdir, blackhole_plasmids,
                                   use_subgraphs=False,
                                   use_subcommunities=False,
                                   show_blackholes_filter=False, show_samples_filter=False, graph_to_sample_to_plasmids=None):
        all_subgraphs = []
        subgraphs_blackhole_plasmids = []
        subgraph_to_sample_to_plasmids = defaultdict(lambda: defaultdict(set))
        descriptions = []

        for graph_index, graph in enumerate(graphs):
            logging.info(f"Producing graph {graph_index}/{len(graphs)}")
            blackhole_plasmids_for_graph = set(blackhole_plasmids[graph_index] if blackhole_plasmids is not None else [])

            # fix_node_to_subcommunity_attributes(graph, plasmid_to_subcommunity, blackhole_plasmids_for_graph)
            graph.fix_node_attributes()

            sample_to_plasmids = graph_to_sample_to_plasmids.get(graph_index) if graph_to_sample_to_plasmids else None

            if use_subgraphs or use_subcommunities:

                # TODO: I am not it is a good idea to remove blackhole plasmids here, for now let's keep this...
                graph.remove_nodes_from(blackhole_plasmids_for_graph)

                subgraphs = graph.get_subgraphs(plasmid_to_subcommunity, use_subgraphs)

                for subgraph_index, subgraph in subgraphs.items():
                    # populates all subgraphs variables
                    all_subgraphs.append(subgraph)

                    blackhole_plasmids_for_subgraph = blackhole_plasmids_for_graph.intersection(list(subgraph))
                    subgraphs_blackhole_plasmids.append(blackhole_plasmids_for_subgraph)

                    subgraph_sample_to_plasmids = None
                    all_subgraphs_index = len(all_subgraphs)-1
                    if sample_to_plasmids is not None:
                        subgraph_sample_to_plasmids = defaultdict(set)
                        for sample, plasmids in sample_to_plasmids.items():
                            for plasmid in plasmids:
                                if plasmid in subgraph:
                                    subgraph_sample_to_plasmids[sample].add(plasmid)
                        subgraph_to_sample_to_plasmids[all_subgraphs_index] = subgraph_sample_to_plasmids

                    description = f"graph_{graph_index}_subgraph_{subgraph_index}"
                    descriptions.append(description)

                    subgraph.produce_visualisation(visualisation_outdir / "graphs", description,
                                          nb_of_black_holes=len(blackhole_plasmids_for_subgraph),
                                          show_blackholes_filter=show_blackholes_filter,
                                          show_samples_filter=show_samples_filter,
                                          sample_to_plasmids=subgraph_sample_to_plasmids)
            else:  # normal graphs (no subgraph/subcommunities)
                description = f"graph_{graph_index}"
                descriptions.append(description)
                graph.produce_visualisation(visualisation_outdir / "graphs", description,
                                  nb_of_black_holes=len(blackhole_plasmids_for_graph),
                                  show_blackholes_filter=show_blackholes_filter, show_samples_filter=show_samples_filter,
                                  sample_to_plasmids=sample_to_plasmids)

        logging.info("Producing index file...")
        if use_subgraphs or use_subcommunities:
            object_description = "subgraphs" if use_subgraphs else "subcommunity"
            OutputProducer.produce_index_file(visualisation_outdir, all_subgraphs, descriptions, object_description, subgraphs_blackhole_plasmids, subgraph_to_sample_to_plasmids)
        else:
            OutputProducer.produce_index_file(visualisation_outdir, graphs, descriptions, "community", blackhole_plasmids, graph_to_sample_to_plasmids)
        logging.info("Producing index file - done!")

    @staticmethod
    def produce_graph_visualisation(graph: BaseGraph, html_path: Path):
        outdir = html_path.parent
        outdir.mkdir(exist_ok=True, parents=True)

        html = graph.produce_visualisation()
        html_path.write_text(html)

        OutputProducer.copy_libs(outdir)
            OutputProducer.copy_libs(outdir)

    @staticmethod
    def copy_libs(outdir):
        shutil.copytree(get_libs_dir(), outdir / "libs", dirs_exist_ok=True)
