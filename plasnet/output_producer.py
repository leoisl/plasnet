import shutil
from pathlib import Path

from plasnet.base_graph import BaseGraph
from plasnet.blackhole_graph import BlackholeGraph
from plasnet.communities import Communities
from plasnet.list_of_graphs import ListOfGraphs
from plasnet.Templates import Templates
from plasnet.utils import get_libs_dir


class OutputProducer:
    @staticmethod
    def produce_graph_visualisation(graph: BaseGraph, html_path: Path) -> None:
        outdir = html_path.parent
        outdir.mkdir(exist_ok=True, parents=True)

        html = graph.produce_visualisation()
        html_path.write_text(html)

        OutputProducer.copy_libs(outdir)

    @staticmethod
    def produce_communities_visualisation(communities: Communities, outdir: Path) -> None:
        OutputProducer._write_html_for_all_subgraphs(communities, outdir)
        OutputProducer._produce_index_file(outdir, communities, "Communities")

    @staticmethod
    def produce_subcommunities_visualisation(
        subcommunities: ListOfGraphs[BlackholeGraph], outdir: Path
    ) -> None:
        OutputProducer._write_html_for_all_subgraphs(subcommunities, outdir)
        OutputProducer._produce_index_file(outdir, subcommunities, "subcommunity")

    @classmethod
    def _write_html_for_all_subgraphs(
        cls, subgraphs: ListOfGraphs[BaseGraph], outdir: Path
    ) -> None:
        graphs_dir = outdir / "graphs"
        graphs_dir.mkdir(exist_ok=True, parents=True)

        for subgraph_index, subgraph in enumerate(subgraphs):
            html = subgraph.produce_visualisation()
            html_path = graphs_dir / f"{subgraph.label}.html"
            html_path.write_text(html)
            relative_html_path = Path(f"graphs/{subgraph.label}.html")
            subgraph.path = relative_html_path

    @staticmethod
    def _produce_index_file(
        outdir: Path, graphs: ListOfGraphs[BlackholeGraph], objects_description: str
    ) -> None:
        sorted_graphs = graphs.get_graphs_sorted_by_size()
        index_src = Templates.read_template("index_template")

        visualisation_links = []
        for graph in sorted_graphs:
            visualisation_links.append(
                f'<a href="{graph.path}" target="_blank">View {graph.description} <br/>'
            )

        with open(outdir / "index.html", "w") as index_fh:
            for line in index_src:
                line = line.replace("<communities_links_tag>", "\n".join(visualisation_links))
                line = line.replace("<objects_description>", objects_description)
                print(line, file=index_fh)

        OutputProducer.copy_libs(outdir)

    @staticmethod
    def copy_libs(outdir: Path) -> None:
        shutil.copytree(get_libs_dir(), outdir / "libs", dirs_exist_ok=True)
