
import pandas as pd
from backend.src.strategies.matchmaking.abstract_class.machmaking_strategy_base import MatchmakingBase

class Strategy(MatchmakingBase):
    def __init__(self, path):
        self.__dataset_path = path
    @property
    def dataset_path(self):
        return self.__dataset_path
    
    @dataset_path.setter
    def dataset_path(self, path):
        self.__dataset_path = path
    
    ## get_offline_user_id() <- change it to..
    def perform_matchmaking(self, current_ratings):
        ## matchmaking logic here
        ## match with the random user in the db
        ## find out the related dataset by the given id



        ## send the movie id only
        rand_user_id_int = 456
        return rand_user_id_int
