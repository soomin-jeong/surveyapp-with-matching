from backend.src.strategies.evaluation.evaluation import EvaluationOfStrategies
from backend.src.strategies.next_question_selection.implemented_strategies.favorite_item_strategy import \
            Strategy as questioning_favorite
from backend.src.strategies.next_question_selection.implemented_strategies.random_selection_strategy import \
            Strategy as questioning_random
from backend.src.strategies.next_question_selection.implemented_strategies.maniac_strategy import \
            Strategy as questioning_maniac

from backend.src.strategies.matchmaking.implemented_strategies.random_matchmaking_strategy import \
            Strategy as matching_random
from backend.src.strategies.matchmaking.implemented_strategies.least_diff_matching_strategy import \
            Strategy as matching_least_diff


# test_dataset_name = 'test2'
test_dataset_name = 'movielens_small'

test_repeating_times = 1000

# ev = EvaluationOfStrategies(test_dataset_name, questioning_favorite, matching_least_diff)
# ratio = ev.get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy(repeating_times=test_repeating_times)
# print("RESULT(dataset={}, n_repeating_times={}, questioning={}, matching={}): \t{}".format(test_dataset_name,
#                                                                                            test_repeating_times,
#                                                                                          questioning_favorite.strategy_name,
#                                                                                          matching_least_diff.strategy_name,
#                                                                                          ratio))
#
# ev2 = EvaluationOfStrategies(test_dataset_name, questioning_random, matching_least_diff)
# ratio = ev.get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy(repeating_times=test_repeating_times)
# print("RESULT(dataset={}, n_repeating_times={}, questioning={}, matching={}): \t{}".format(test_dataset_name,
#                                                                                test_repeating_times,
#                                                                              questioning_random.strategy_name,
#                                                                              matching_least_diff.strategy_name,
#                                                                              ratio))



ev = EvaluationOfStrategies(test_dataset_name, questioning_favorite, matching_random)
ratio = ev.get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy(repeating_times=test_repeating_times)
print("RESULT(dataset={}, n_repeating_times={}, questioning={}, matching={}): \t{}".format(test_dataset_name,
                                                                                           test_repeating_times,
                                                                                         questioning_favorite.strategy_name,
                                                                                         matching_random.strategy_name,
                                                                                         ratio))

ev2 = EvaluationOfStrategies(test_dataset_name, questioning_random, matching_random)
ratio = ev.get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy(repeating_times=test_repeating_times)
print("RESULT(dataset={}, n_repeating_times={}, questioning={}, matching={}): \t{}".format(test_dataset_name,
                                                                               test_repeating_times,
                                                                             questioning_random.strategy_name,
                                                                             matching_random.strategy_name,
                                                                             ratio))


ev = EvaluationOfStrategies(test_dataset_name, questioning_maniac, matching_random)
ratio = ev.get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy(repeating_times=test_repeating_times)
print("RESULT(dataset={}, n_repeating_times={}, questioning={}, matching={}): \t{}".format(test_dataset_name,
                                                                                           test_repeating_times,
                                                                                         questioning_maniac.strategy_name,
                                                                                         matching_random.strategy_name,
                                                                                         ratio))


