import os

from backend.src.strategies.next_question_selection.abstract_class.item_selection_base_choice import BaseStrategyChoice
from backend.src.utils.utils import convert_current_ratings_str_into_list

from backend.src.strategies.preprocessing.hierarchical_clustering import UserCluster
from backend.src.strategies.next_question_selection.user_cluster_with_representative_item import UserClusterRep, \
    get_cluster_matched_up_to_now


class Strategy(BaseStrategyChoice):
    strategy_name = 'maniac'

    def __init__(self, dataset_name: str):
        super(Strategy, self).__init__(dataset_name)

