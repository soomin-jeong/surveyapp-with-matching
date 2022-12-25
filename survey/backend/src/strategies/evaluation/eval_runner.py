import time

from backend.src.strategies.evaluation.evaluation import EvaluationOfStrategies
from backend.src.strategies.next_question_selection.implemented_strategies.favorite_item_strategy import \
            Strategy as questioning_favorite
from backend.src.strategies.next_question_selection.implemented_strategies.random_selection_strategy import \
            Strategy as questioning_random
from backend.src.strategies.next_question_selection.implemented_strategies.maniac_strategy import \
            Strategy as questioning_maniac
from backend.src.strategies.next_question_selection.implemented_strategies.rated_by_the_most_strategy import \
            Strategy as questioning_rated_most

from backend.src.strategies.matchmaking.implemented_strategies.random_matchmaking_strategy import \
            Strategy as matching_random
from backend.src.strategies.matchmaking.implemented_strategies.least_diff_matching_strategy import \
            Strategy as matching_least_diff


def print_result(dataset_name, repeating_times, questioning_strategies, matching_strategies):
    print("## EVALUATION with dataset [{}] repeating [{}] times".format(dataset_name, repeating_times))

    for each_questioning_strategy in questioning_strategies:
        for each_matching_strategy in matching_strategies:
            start = time.time()
            ev = EvaluationOfStrategies(dataset_name, each_questioning_strategy, each_matching_strategy)
            hit_ratio = ev.get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy(
                repeating_times=repeating_times)
            end = time.time()
            print("Hit Rate (questioning={}, matching={}): \t{} (in {}s)".format(each_questioning_strategy.strategy_name,
                                                                                 each_matching_strategy.strategy_name,
                                                                                 hit_ratio,
                                                                                 round(end-start, 5)))


test_dataset_name = 'movielens_small'
test_repeating_times = 100000

# USER GUIDE: add the  questioning strategies to evaluate here
questioning_strategies = [questioning_random, questioning_favorite, questioning_rated_most, questioning_maniac]
# USER GUIDE: add the  matching strategies to evaluate here
matching_strategies = [matching_random]

print_result(test_dataset_name, test_repeating_times, questioning_strategies, matching_strategies)

