# TODO: refactor
from plasnet.community_graph import CommunityGraph
from plasnet.list_of_graphs import ListOfGraphs
from plasnet.utils import DistanceDict


class Communities(ListOfGraphs[CommunityGraph]):
    def filter_by_distance(
        self, distance_dict: DistanceDict, distance_threshold: float
    ) -> None:
        for community in self:
            community.filter_by_distance(distance_dict, distance_threshold)
