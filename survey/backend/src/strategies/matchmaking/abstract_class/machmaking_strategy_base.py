import pandas as pd

from ...preprocessing.hierarchical_clustering import UserCluster
from abc import abstractmethod, ABCMeta


class MatchmakingBase(metaclass=ABCMeta):

    def __init__(self, matched_cluster: UserCluster, rating_matrix: pd.DataFrame, online_user_rating: dict):
        self.matched_cluster = matched_cluster
        self.rating_matrix = rating_matrix
        self.online_user_rating = online_user_rating

    def get_matched_offline_user_id(self) -> int:
        # when there is only one user in the cluster, match with the user right away
        if self.matched_cluster.user_cnt == 1:
            return self.matched_cluster.user_ids[0]

        else:
            return self.get_matched_user_id_among_multiple_in_cluster()

    @abstractmethod
    def get_matched_user_id_among_multiple_in_cluster(self) -> int:
        raise NotImplementedError("{}.{} should be implemented".format(self.__class__.__name__, self.__module__.__name__))

