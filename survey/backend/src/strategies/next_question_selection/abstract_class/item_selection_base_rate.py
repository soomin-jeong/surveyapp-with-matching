
import abc

from backend.src.strategies.next_question_selection.abstract_class.item_selection_base import BaseStrategy


class abstract_attribute(object):
    def __get__(self, obj, type):
        raise NotImplementedError("This attribute was not set in a subclass")


class BaseStrategyRate(BaseStrategy):

    @abc.abstractmethod
    def get_next_item(self, current_ratings: dict):
        """
            current_ratings: ratings in dict style string (key: movieId, value: rating)
            i.e. {'3211': '4.5'}
        """
        # returns one movie_id in string
        raise NotImplementedError("{} should be implemented".format(self.__class__.__name__))