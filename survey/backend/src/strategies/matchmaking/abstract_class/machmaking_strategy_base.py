from ...preprocessing.hierarchical_clustering import UserCluster
from ....app import db

import pandas as pd
from abc import abstractmethod, ABCMeta


class MatchmakingBase(metaclass=ABCMeta):

    def __init__(self, matched_cluster: UserCluster):
        self.matched_cluster = matched_cluster

    def get_matched_offline_user(self) -> int:
        # when there is only one user in the cluster, match with the user right away
        if self.matched_cluster.user_cnt == 1:
            return self.matched_cluster.user_ids[0]

        else:
            return self.match_one_among_users_in_cluster()

    @abstractmethod
    def match_one_among_users_in_cluster(self) -> int:
        raise NotImplementedError("{}.{} should be implemented".format(self.__class__.__name__, self.__module__.__name__))

