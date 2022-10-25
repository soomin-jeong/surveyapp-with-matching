from ....app import db

import pandas as pd
from abc import abstractmethod, ABC, ABCMeta


class MatchmakingBase(metaclass = ABCMeta):
    @abstractmethod
    def __init__(self, rating_df: pd.DataFrame):
        self.rating_df: pd.DataFrame = rating_df


    @abstractmethod
    def perform_matchmaking(self) -> int:
        pass


