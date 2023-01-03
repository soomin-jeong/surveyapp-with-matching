
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

    @abc.abstractmethod
    def simulate_online_user_response(self, online_user_id: int, candidate_item_id: int) -> int:
        """
        survey/backend/src/strategies/evaluation.py evaluates the performance of questioning strategies by simulating a user's response
        as if we did not know this user's ratings, like limiting training data to test it later in Machine Learning.
        This function simulates an online user's response during evaluation
        given that the online user's rating is already in the ratings data.

        Args:
            online_user_id: id of the online user who will be making the decision when given a question
            candidate_item_id: item id given to rate
        """
        # returns one movie_id in string
        raise NotImplementedError("{}.{} should be implemented".format(self.__class__.__name__, self.__module__.__name__))
