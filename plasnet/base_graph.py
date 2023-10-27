# TODO: requires heavy refactoring

import networkx as nx
from plasnet.ColorPicker import ColorPicker
from plasnet.Templates import Templates
import json
from collections import defaultdict


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

    def _get_node_color(self, node):
        return ColorPicker.get_default_color()

    def _get_node_shape(self, node):
        return "circle"

    def _add_special_node_attributes(self, node, attrs):
        ...

    def fix_node_attributes(self):
        for node, attrs in self.nodes.items():
            attrs["color"] = self._get_node_color(node)
            attrs["shape"] = self._get_node_shape(node)
            self._add_special_node_attributes(node, attrs)

    def get_induced_components(self, nodes):
        subgraph = self.subgraph(nodes)
        return nx.connected_components(subgraph)


    TIME_LIMIT_FOR_SMALL_GRAPHS = 1000
    TIME_LIMIT_FOR_LARGE_GRAPHS = 10000
    def get_simulation_time(self):
        is_a_small_enough_graph = self.number_of_nodes() <= 5 or self.number_of_edges() <= 10
        if is_a_small_enough_graph:
            return self.TIME_LIMIT_FOR_SMALL_GRAPHS
        else:
            return self.TIME_LIMIT_FOR_LARGE_GRAPHS

    def produce_visualisation(self, outdir, label, nb_of_black_holes, show_blackholes_filter=False, show_samples_filter=False,
                              sample_to_plasmids=None):
        outdir.mkdir(parents=True, exist_ok=True)

        visualisation_src = Templates.read_template("visualisation_template")

        graph_as_cy_dict = nx.cytoscape_data(self)
        elements_as_cy_json = json.dumps(graph_as_cy_dict["elements"])

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

        with open(outdir / f"{label}.html", "w") as visualisation_fh:
            for line in visualisation_src:
                line = line.replace("<samples_selectors>", samples_selectors_str)
                line = line.replace("<elements_tag>", elements_as_cy_json)
                line = line.replace("<movementThreshold>", str(self.number_of_edges()))
                line = line.replace("<maxSimulationTime>", str(self.get_simulation_time()))
                line = line.replace("<filters_tag>", "\n".join(filters))
                line = line.replace("<custom_buttons_tag>", "\n".join(custom_buttons))
                print(line, file=visualisation_fh)

    def get_subgraphs(self, plasmid_to_subcommunity, use_subgraphs):
        if use_subgraphs:
            subgraphs = {comp_index: self.subgraph(component).copy() for comp_index, component in enumerate(nx.connected_components(self))}
        else:
            components = defaultdict(list)
            for plasmid in self:
                subcommunity = plasmid_to_subcommunity[plasmid]
                components[subcommunity].append(plasmid)
            subgraphs = {comp_index: self.subgraph(component).copy() for comp_index, component in components.items()}

        return subgraphs


