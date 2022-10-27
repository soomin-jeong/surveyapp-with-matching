
import pandas as pd
from .abstract_class.machmaking_strategy_base import MatchmakingBase


class Strategy(MatchmakingBase):
    def __init__(self, rating_df: pd.DataFrame):
        self.rating_df = rating_df

    def get_matched_offline_user(self) -> int:
        ## matchmaking logic here
        ## match with the random user in the db
        ## find out the related dataset by the given id

        ## select a random item
        item = self.rating_df.sample(axis="rows")

        rand_user_id_int = int(item['userId'].values[0])
        return rand_user_id_int
