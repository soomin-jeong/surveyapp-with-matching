import random

from backend.src.strategies.next_question_selection.abstract_class.item_selection_base_choice import BaseStrategyChoice as QuestioningBase
from backend.src.strategies.matchmaking.abstract_class.machmaking_strategy_base import BaseStrategy as MatchmakingBase

from backend.src.strategies.next_question_selection.implemented_strategies.favorite_item_strategy import \
            Strategy as s_favorite

from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster, UserCluster


class EvaluationOfStrategies:
    def __init__(self, n_times: int, dataset_name: str, questioning_strategy: QuestioningBase, matchmaking_strategy: MatchmakingBase):
        self.dataset_name = dataset_name
        self.n_times = n_times
        self.questioning_strategy = questioning_strategy
        self.matchmaking_strategy = matchmaking_strategy

    def _pick_online_user_id(self, user_cluster: UserCluster):
        return random.choice(user_cluster.user_ids)

    def find_offline_user_id_matching(self, online_user_id: int):
        offline_user_id = 1
        return offline_user_id

    def get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy(self):
        hit_times = 0

        for n in range(self.n_times):
            online_user_id = self._pick_online_user_id(self.questioning_strategy.clustering.root_cluster)
            offline_user_id = self.find_offline_user_id_matching(online_user_id)
            if online_user_id == offline_user_id:
                hit_times += 1

        return hit_times / self.n_times




