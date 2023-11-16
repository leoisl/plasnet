from plasnet.list_of_graphs import ListOfGraphs
from plasnet.sample_graph import SampleGraph


class ListOfSampleGraphs(ListOfGraphs[SampleGraph]):
    def get_graphs_sorted_by_size(self) -> "ListOfSampleGraphs":
        nb_of_hit_samples = map(SampleGraph.get_number_of_hit_samples, self)

        graphs_and_nb_of_hit_samples = [
            (graph, nb_of_hit_samples) for graph, nb_of_hit_samples in zip(self, nb_of_hit_samples)
        ]

        graphs_and_nb_of_hit_samples_sorted = sorted(
            graphs_and_nb_of_hit_samples, key=lambda x: x[1], reverse=True
        )
        sorted_graphs = [graph for graph, _ in graphs_and_nb_of_hit_samples_sorted]
        return ListOfSampleGraphs(sorted_graphs)
