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