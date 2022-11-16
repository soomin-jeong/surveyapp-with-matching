import ast
import json
import pandas as pd
import numpy as np
import random

from backend.src.strategies.next_question_selection.abstract_class.item_selection_base import BaseStrategy
from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster


class Strategy(BaseStrategy):
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.clustering = HierarchicalCluster(dataset_name)

    def get_next_items(self, current_ratings: str) -> int:
        current_ratings_dict = ast.literal_eval(current_ratings)

        if current_ratings:
            rated_item_ids = [int(each) for each in current_ratings_dict.keys()]
        else:
            rated_item_ids = []

        ## select a random item except the items already rated
        items_available_to_rate = [each_item for each_item in self.cluster.rating_matrix_na_filled.columns
                                   if each_item not in rated_item_ids]

        next_item = random.choice(items_available_to_rate)
        return next_item


