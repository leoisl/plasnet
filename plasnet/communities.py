# TODO: refactor
from plasnet.community_graph import CommunityGraph
from plasnet.list_of_graphs import ListOfGraphs
from plasnet.utils import DistanceDict


class Communities(ListOfGraphs[CommunityGraph]):
    def add_typing_distances(self, distance_dict: DistanceDict) -> None:
        for community in self:
            community.add_typing_distances(distance_dict)

    def filter_by_distance(self, distance_threshold: float) -> None:
        for community in self:
            community.filter_by_distance(distance_threshold)
