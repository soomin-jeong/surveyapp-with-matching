
import pandas as pd
from .abstract_class.machmaking_strategy_base import MatchmakingBase

class NaiveStrategy(MatchmakingBase):
    def __init__(self, rating_df: pd.DataFrame):
        self.rating_df = rating_df

    ## get_offline_user_id() <- change it to..
    def perform_matchmaking(self):
        ## matchmaking logic here
        ## match with the random user in the db
        ## find out the related dataset by the given id

        ## select a random item
        item = self.rating_df.sample(axis="rows")

        rand_user_id_int = int(item['userId'].values[0])
        return rand_user_id_int
