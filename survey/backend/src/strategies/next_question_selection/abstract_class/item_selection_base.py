
import abc
import pandas as pd


## abstract SQLAlchemy Model class
## this class does not exist as table in db, only the instantiations do


class BaseStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, rating_df: pd.DataFrame):
        self.rating_df: pd.DataFrame = rating_df

    @abc.abstractmethod
    def get_next_item(self, current_ratings) -> str:
        # returns one movie_id in string
        pass