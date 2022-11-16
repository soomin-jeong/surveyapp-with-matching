import json
import pandas as pd
import numpy as np
import random
import ast

from backend.src.strategies.next_question_selection.abstract_class.item_selection_base import BaseStrategy
from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from backend.src.strategies.preprocessing.utils import raw_dataset_path


def get_representative_item(df_items_rated_by_the_cluster: pd.DataFrame):
    # if the representative items are redundant, replace it with the next level
    rating_cnt_per_item = df_items_rated_by_the_cluster.count()
    # sort it ascending and pick the last one
    return rating_cnt_per_item.sort_values().keys()[-1]


class Strategy(BaseStrategy):
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.clustering = HierarchicalCluster(dataset_name)

    def get_next_items(self, current_ratings: str) -> [int]:
        
        ## convert the chosen items as string into list
        if current_ratings == "[]" or current_ratings is None:
            already_rated_items = []
        else:
            already_rated_items = current_ratings[1:-1].split(',')

        depth = len(current_ratings)

        curr_cluster = self.clustering.root_cluster


        for each_level in range(depth-1):
            child_clusters = curr_cluster.child_clusters

            representative_items_at_this_level = []

            for each_cluster in child_clusters:
                representative_item_of_cluster = get_representative_item(self.clustering.rating_matrix.loc[each_cluster.user_ids])
                representative_items_at_this_level.append(representative_item_of_cluster)
            # the chosen item at kth question tells which cluster was chosen
            chosen_cluster_index = representative_items_at_this_level.index(already_rated_items[each_level])
            curr_cluster = child_clusters[chosen_cluster_index]

        # get the representative items of curr_cluster and return
        next_items = []

        for each_cluster in curr_cluster.child_clusters:
            # select item ratings by the users in each cluster in the data frame
            df_items_rated_by_the_cluster = self.clustering.rating_matrix.filter(items=each_cluster.user_ids, axis='rows')

            # count the non-null values of each column, and pick the columns with the most non-null values
            most_rated_item = get_representative_item(df_items_rated_by_the_cluster)

            # add it to the next_items
            next_items.append(most_rated_item)

        return next_items
    


