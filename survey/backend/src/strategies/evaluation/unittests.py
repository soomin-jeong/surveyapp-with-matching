import unittest
from backend.src.strategies.evaluation.evaluation import EvaluationOfStrategies
from backend.src.strategies.next_question_selection.implemented_strategies.favorite_item_strategy import \
            Strategy as questioning_favorite
from backend.src.strategies.matchmaking.implemented_strategies.random_matchmaking_strategy import \
            Strategy as matching_random


class EvaluationTest(unittest.TestCase):

    def test_add_new_response_to_empty_str(self):
        ev = EvaluationOfStrategies('test1', questioning_favorite, matching_random)
        self.assertEqual(ev._add_new_response_to_str("[]", 1), "[1]")

    def test_add_new_response_to_str_with_responses(self):
        ev = EvaluationOfStrategies('test1', questioning_favorite, matching_random)
        self.assertEqual(ev._add_new_response_to_str("[13]", 14), "[13,14]")

    def test_add_new_response_to_str_with_many_responses(self):
        ev = EvaluationOfStrategies('test1', questioning_favorite, matching_random)
        self.assertEqual(ev._add_new_response_to_str("[13,12,19,291]", 1234), "[13,12,19,291,1234]")

    def test_add_new_response_to_str_with_same_responses(self):
        ev = EvaluationOfStrategies('test1', questioning_favorite, matching_random)
        self.assertEqual(ev._add_new_response_to_str("[13,12,19,291]", 13), "[13,12,19,291,13]")
