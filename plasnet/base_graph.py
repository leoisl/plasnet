import json
import pickle
from abc import abstractmethod
from collections import defaultdict
from pathlib import Path
from typing import TextIO

import networkx as nx

from plasnet.ColorPicker import ColorPicker
from plasnet.Templates import Templates


class BaseGraph(nx.Graph):
    """
    Class to represent a base class to concentrate common methods between the different types of graphs.
    """

    # def fix_node_to_subcommunity_attributes(self, node_to_subcommunity, blackhole_plasmids):
    #     for node, attrs in self.nodes.items():
    #         if node in node_to_subcommunity:
    #             attrs["color"] = ColorPicker.get_color_given_index(node_to_subcommunity[node])
    #         else:
    #             attrs["color"] = ColorPicker.get_default_color()
    #
    #         if node in blackhole_plasmids:
    #             attrs["shape"] = "star"
    #             attrs["is_blackhole"] = True
    #         else:
    #             attrs["is_blackhole"] = False

    def __init__(self, graph: nx.Graph = None, label: str = "") -> None:
        super().__init__(graph)
        self._label = label

    @property
    def label(self) -> str:
        return self._label

    def _get_node_color(self, node: str) -> str:
        return ColorPicker.get_default_color()

    def _get_node_shape(self, node: str) -> str:
        return "circle"

    def _add_special_node_attributes(self, node: str, attrs: dict[str, str]) -> None:
        ...

    def remove_plasmids(self, plasmids_to_be_removed: list[str]) -> None:
        self.remove_nodes_from(plasmids_to_be_removed)

    def fix_node_attributes(self) -> None:
        for node, attrs in self.nodes.items():
            attrs["color"] = self._get_node_color(node)
            attrs["shape"] = self._get_node_shape(node)
            self._add_special_node_attributes(node, attrs)

    def get_induced_components(self, nodes: list[str]) -> "BaseGraph":
        subgraph = self.subgraph(nodes)
        return nx.connected_components(subgraph)

    TIME_LIMIT_FOR_SMALL_GRAPHS = 1000
    TIME_LIMIT_FOR_LARGE_GRAPHS = 10000

    def get_simulation_time(self) -> int:
        is_a_small_enough_graph = self.number_of_nodes() <= 5 or self.number_of_edges() <= 10
        if is_a_small_enough_graph:
            return self.TIME_LIMIT_FOR_SMALL_GRAPHS
        else:
            return self.TIME_LIMIT_FOR_LARGE_GRAPHS

    def produce_visualisation(self) -> str:
        self.fix_node_attributes()
        visualisation_src = Templates.read_template("visualisation_template")

        graph_as_cy_dict = nx.cytoscape_data(self)
        elements_as_cy_json = json.dumps(graph_as_cy_dict["elements"])

        """
        if sample_to_plasmids:
            samples_selectors = []
            for sample, plasmids in sample_to_plasmids.items():
                induced_components = self.get_induced_components(plasmids)
                for component_index, component in enumerate(induced_components):
                    node_selector = [f"node#{node}" for node in component]
                    node_selector = ", ".join(node_selector)
                    if component_index==0:
                        samples_selectors.append(f"sample_selector_nodes['{sample}'] = [];")
                    samples_selectors.append(f"sample_selector_nodes['{sample}'].push(cy.elements('{node_selector}'));")
            samples_selectors_str = "\n".join(samples_selectors)

            sample_hits_checkboxes = []
            for sample_index, sample in enumerate(sample_to_plasmids):
                colour = ColorPicker.get_color_given_index(sample_index)
                sample_hits_checkboxes.append(
                    f'<input type="checkbox" id="{sample}" name="{sample}" onclick="show_sample_hits(\'{sample}\', \'{colour}\')">'
                    f'<label for="{sample}">{sample} ({len(sample_to_plasmids[sample])} hits) <span style="color:{colour}">&#9632;</span></label><br/>'
                )
        else:
            samples_selectors_str = ""
            sample_hits_checkboxes = []


        filters = []
        if show_blackholes_filter:
            filters.append(f'<label for="hide_blackholes">Hide blackhole plasmids ({nb_of_black_holes} present)</label>'
                           f'<input type="checkbox" id="hide_blackholes" name="hide_blackholes"><br/>')
        if show_samples_filter:
            filters.append("Show hits for samples:<br/>")
            filters.extend(sample_hits_checkboxes)

        custom_buttons = []
        if show_blackholes_filter:
            custom_buttons.append('<div><input type="submit" value="Redraw" onclick="redraw()"></div>')
        """  # noqa: E501

        # [CRITICAL] TODO: improve this horrible performance
        libs_relative_path = self._get_libs_relative_path()
        samples_selectors = self._get_samples_selectors_HTML()
        filters = self._get_filters_HTML()
        custom_buttons = self._get_custom_buttons_HTML()

        final_html_lines = []
        for line in visualisation_src:
            line = line.replace("<libs_relative_path>", libs_relative_path)
            line = line.replace("<samples_selectors>", samples_selectors)
            line = line.replace("<elements_tag>", elements_as_cy_json)
            line = line.replace("<movementThreshold>", str(self.number_of_edges()))
            line = line.replace("<maxSimulationTime>", str(self.get_simulation_time()))
            line = line.replace("<filters_tag>", filters)
            line = line.replace("<custom_buttons_tag>", custom_buttons)
            final_html_lines.append(line)

        return "\n".join(final_html_lines)

    @abstractmethod
    def _get_libs_relative_path(self) -> str:
        ...

    @abstractmethod
    def _get_samples_selectors_HTML(self) -> str:
        ...

    @abstractmethod
    def _get_filters_HTML(self) -> str:
        ...

    @abstractmethod
    def _get_custom_buttons_HTML(self) -> str:
        ...

    def save(self, filepath: Path) -> None:
        with open(filepath, "wb") as fh:
            pickle.dump(self, fh)

    @staticmethod
    def load(filepath):
        with open(filepath, "rb") as fh:
            graph = pickle.load(fh)
            return graph

    def write_classification(self, typing_fh: TextIO) -> None:
        for node in self.nodes:
            typing_fh.write(f"{node}\t{self.label}\n")
