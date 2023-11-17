from typing import Optional

import networkx as nx
import pandas as pd

from plasnet.ColorPicker import ColorPicker
from plasnet.subcommunity_graph import SubcommunityGraph


class SampleGraph(SubcommunityGraph):
    def __init__(
        self,
        graph: Optional[nx.Graph] = None,
        blackhole_connectivity_threshold: int = 0,
        edge_density: float = 0.0,
        label: str = "",
        colour: str = ColorPicker.get_default_color(),
        sample_plasmid: Optional[pd.DataFrame] = None,
    ):
        super().__init__(graph, blackhole_connectivity_threshold, edge_density, label, colour)
        if sample_plasmid is not None:
            self._sample_to_plasmids = (
                sample_plasmid.groupby("sample")["plasmid"].apply(list).to_dict()
            )

    @classmethod
    def from_subcommunity_graph(
        cls, subcommunity_graph: SubcommunityGraph, sample_plasmid: pd.DataFrame
    ) -> "SampleGraph":
        return cls(
            subcommunity_graph,
            subcommunity_graph._blackhole_connectivity_threshold,
            subcommunity_graph._edge_density,
            subcommunity_graph.label,
            subcommunity_graph._colour,
            sample_plasmid,
        )

    def get_number_of_hit_samples(self) -> int:
        return len(self._sample_to_plasmids)

    def _get_samples_selectors_HTML(self) -> str:
        samples_selectors = []
        for sample, plasmids in self._sample_to_plasmids.items():
            induced_components = self.get_induced_components(plasmids)
            for component_index, component in enumerate(induced_components):
                node_selector = [f"node#{node}" for node in component]
                if component_index == 0:
                    samples_selectors.append(f"sample_selector_nodes['{sample}'] = [];")
                node_selector_str = ", ".join(node_selector)
                samples_selectors.append(
                    f"sample_selector_nodes['{sample}'].push(cy.elements('{node_selector_str}'));"
                )
        samples_selectors_str = "\n".join(samples_selectors)
        return samples_selectors_str

    def _get_filters_HTML(self) -> str:
        previous_filters = super()._get_filters_HTML()

        sample_hits_checkboxes = []
        for sample_index, sample in enumerate(self._sample_to_plasmids):
            colour = ColorPicker.get_color_given_index(sample_index)
            sample_hits_checkboxes.append(
                f'<input type="checkbox" id="{sample}" name="{sample}" '
                f"onclick=\"show_sample_hits('{sample}', '{colour}')\">"
                f'<label for="{sample}">{sample} ({len(self._sample_to_plasmids[sample])} hits) '
                f'<span style="color:{colour}">&#9632;</span></label><br/>'
            )

        html_filters = (
            f"{previous_filters}<br/>"
            f"Show hits for samples:<br/>"
            f"{''.join(sample_hits_checkboxes)}"
        )
        return html_filters

    @property
    def description(self) -> str:
        description = super().description
        description += f" - {self.get_number_of_hit_samples()} samples hit"
        return description
