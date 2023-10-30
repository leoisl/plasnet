# TODO: refactor

from community_graph import CommunityGraph
import pickle


class Communities(list[CommunityGraph]):
    """
    Represents plasmid communities
    """

    def save(self, communities_filepath):
        with open(communities_filepath, "wb") as fh:
            pickle.dump(self, fh)

    @staticmethod
    def load(communities_filepath) -> "Communities":
        with open(communities_filepath, "rb") as fh:
            communities = pickle.load(fh)
            return communities
