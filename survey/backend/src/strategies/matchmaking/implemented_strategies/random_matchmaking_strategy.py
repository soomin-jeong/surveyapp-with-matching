
from numpy import random
from backend.src.strategies.matchmaking.abstract_class.matching_strategy_base import BaseStrategy


class Strategy(BaseStrategy):
    strategy_name = 'random'

    def get_matched_user_id_among_multiple_in_cluster(self) -> int:
        reproducible_random_state = random.RandomState(97)
        return int(reproducible_random_state.choice(self.matched_cluster.user_ids))
