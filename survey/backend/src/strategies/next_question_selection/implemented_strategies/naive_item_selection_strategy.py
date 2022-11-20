import random

from backend.src.strategies.next_question_selection.abstract_class.item_selection_base import BaseStrategy
from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from backend.src.utils.utils import convert_current_ratings_str_into_list


class Strategy(BaseStrategy):
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.clustering = HierarchicalCluster(dataset_name)

    def has_next(self, choices_so_far_str: str) -> bool:
        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)
        return len(choices_so_far) < self.clustering.rating_matrix_na_filled.columns

    def get_next_items(self, choices_so_far_str: str) -> [int]:
        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)

        ## select a random item except the items already rated
        items_available_to_rate = [each_item for each_item in self.clustering.rating_matrix_na_filled.columns
                                   if each_item not in choices_so_far]

        # pick 2 items (as it should return at least 2 items to choose from) by sampling without replacement
        next_items = random.sample(population=items_available_to_rate, k=2)
        return next_items


