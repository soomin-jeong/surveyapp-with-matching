import random
import pandas as pd

from backend.src.strategies.matchmaking.abstract_class.matching_strategy_base import BaseStrategy
from backend.settings import MAX_RATING
from backend.src.utils.utils import convert_current_ratings_str_into_list

SQAURED_DIFF_COL_NAME = 'squared_diff'


def deduct_by_online_user_ratings(ratings_by_matched_cluster: pd.DataFrame, online_user_ratings: [int]):
    ratings_by_matched_cluster = ratings_by_matched_cluster.fillna(-1)
    ratings_by_matched_cluster[SQAURED_DIFF_COL_NAME] = 0

    for each_item_id in online_user_ratings:

        # defensive code where the items that the online user rated does not exist
        # in the ratings of the offline users
        if each_item_id in ratings_by_matched_cluster.columns:
            rating_diff = ratings_by_matched_cluster[each_item_id] - MAX_RATING
            ratings_by_matched_cluster[SQAURED_DIFF_COL_NAME] += pow(rating_diff, 2)

    return ratings_by_matched_cluster


class Strategy(BaseStrategy):
    strategy_name = 'least_diff'

    def get_matched_user_id_among_multiple_in_cluster(self) -> int:
        candidates_to_match = self.matched_cluster.user_ids

        if len(candidates_to_match) == 1:
            return candidates_to_match[0]

        else:
            online_user_rating_items_list = set(convert_current_ratings_str_into_list(self.online_user_rating))
            ratings_by_matched_cluster = self.rating_matrix.filter(items=candidates_to_match, axis=0)[online_user_rating_items_list]
            ratings_with_squared_error = deduct_by_online_user_ratings(ratings_by_matched_cluster, online_user_rating_items_list)
            users_with_least_square_error = ratings_with_squared_error[ratings_with_squared_error[SQAURED_DIFF_COL_NAME] == min(ratings_with_squared_error[SQAURED_DIFF_COL_NAME])].index
            return int(random.choice(users_with_least_square_error))

