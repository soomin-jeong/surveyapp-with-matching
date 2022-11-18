
import abc
import pandas as pd

## abstract SQLAlchemy Model class
## this class does not exist as table in db, only the instantiations do


class BaseStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("{} should be implemented".format(self.__class__.__name__))

    @abc.abstractmethod
    def get_next_items(self,  *args, **kwargs) -> [int]:
        """
        Args may contain...
            current_ratings: ratings in dict style string (key: movieId, value: rating)
            i.e. {'3211': '4.5'}
            choices_so_far: items that are chosen based on the question (i.e. What's your favorite item among the following?)
            i.e. ['3211', '412']
        """
        # returns one movie_id in string
        raise NotImplementedError("{} should be implemented".format(self.__class__.__name__))