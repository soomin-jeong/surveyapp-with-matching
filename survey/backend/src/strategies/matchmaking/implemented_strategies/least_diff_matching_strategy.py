
import pandas as pd

from backend.src.strategies.matchmaking.abstract_class.machmaking_strategy_base import MatchmakingBase

SQAURED_DIFF_COL_NAME = 'squared_diff'


def deduct_by_online_user_ratings(ratings_by_matched_cluster: pd.DataFrame, online_user_rating: dict):
    ratings_by_matched_cluster = ratings_by_matched_cluster.fillna(-1)
    ratings_by_matched_cluster[SQAURED_DIFF_COL_NAME] = 0

    for each_item_id in online_user_rating.keys():

        # defending cases where the items that the online user rated does not exist
        # in the ratings of the offline users
        if each_item_id in ratings_by_matched_cluster.columns:
            rating_diff = ratings_by_matched_cluster[each_item_id] - online_user_rating.get(each_item_id)
            ratings_by_matched_cluster[SQAURED_DIFF_COL_NAME] += pow(rating_diff, 2)

    return ratings_by_matched_cluster


class Strategy(MatchmakingBase):

    def get_matched_user_id_among_multiple_in_cluster(self) -> int:
        ratings_by_matched_cluster = self.rating_matrix.filter(items=self.matched_cluster.user_ids, axis=0)
        ratings_by_matched_cluster_with_diff = deduct_by_online_user_ratings(ratings_by_matched_cluster, self.online_user_rating)
        user_id_with_smallest_squared_diff = int(ratings_by_matched_cluster_with_diff[SQAURED_DIFF_COL_NAME].sort_values(ascending=True).first_valid_index())
        return user_id_with_smallest_squared_diff

