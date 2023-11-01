# TODO: refactor
from plasnet.list_of_graphs import ListOfGraphs


class Communities(ListOfGraphs):
    def filter_by_distance(self, distance_dict, distance_threshold):
        for community in self:
            community.filter_by_distance(distance_dict, distance_threshold)
