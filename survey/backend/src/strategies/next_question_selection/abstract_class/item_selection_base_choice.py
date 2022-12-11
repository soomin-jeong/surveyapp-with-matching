import abc
from backend.src.strategies.next_question_selection.abstract_class.item_selection_base import BaseStrategy


class BaseStrategyChoice(BaseStrategy):

    @abc.abstractmethod
    def get_next_items(self,  choices_so_far_str: str) -> [int]:
        """
        Args:
            choices_so_far: list of item ids in string, which contains items that are chosen based on the question (i.e. What's your favorite item among the following?)
            i.e. "[3211, 412]"
        """
        # returns one movie_id in string
        raise NotImplementedError("{}.{} should be implemented".format(self.__class__.__name__, self.__module__.__name__))

    @abc.abstractmethod
    def simulate_online_user_response(self, online_user_id: int, candidate_item_ids: [int]) -> int:
        """
        survey/backend/src/strategies/evaluation.py evaluates the performance of questioning strategies by simulating a user's response
        as if we did not know this user's ratings, like limiting training data to test it later in Machine Learning.
        This function simulates an online user's response during evaluation
        given that the online user's rating is already in the ratings data.

        Args:
            online_user_id: id of the online user who will be making the decision when given a question
            candidate_item_ids: ids of items given as options to choose from

        i.e. when the survey application shows 5 items (id = 11, 12, 13, 14, 15),
        this function will return the id of the item which online user will choose from these items
        """
        # returns one movie_id in string
        raise NotImplementedError("{}.{} should be implemented".format(self.__class__.__name__, self.__module__.__name__))
