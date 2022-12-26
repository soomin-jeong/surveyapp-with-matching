import time

import numpy as np
import scipy.stats as stats


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


def print_eval_result(dataset_name, repeating_times, questioning_strategies, matching_strategies):
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


def print_t_test_result(dataset_name, questioning_strategies, sample_size, n_samples):
    '''

    Returns:
        Rejects N0 : Rejects null hypothesis; hence, it is meaningful
        Accept N0 : Accepts null hypothesis; hence, it is NOT meaningful

    '''

    def collect_hit_ratio(dataset_name, questioning_strategy, matching_strategy, sample_size: int, n_samples: int):
        hit_ratio_samples = []

        for each_sampling in range(n_samples):
            control_ev = EvaluationOfStrategies(dataset_name, questioning_strategy, matching_strategy)
            hit_ratio = control_ev.get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy(
                repeating_times=sample_size)
            hit_ratio_samples.append(hit_ratio)

        return hit_ratio_samples

    BASE_MATCHING_STRATEGY = matching_random
    CONTROL_GROUP_QUESTIONING_STRATEGY = questioning_random

    control_hit_ratios = collect_hit_ratio(dataset_name, CONTROL_GROUP_QUESTIONING_STRATEGY,
                                           BASE_MATCHING_STRATEGY, sample_size, n_samples)

    for each_q_strategy in questioning_strategies:
        test_hit_ratios = collect_hit_ratio(dataset_name, each_q_strategy,
                                            BASE_MATCHING_STRATEGY, sample_size, n_samples)

        t_test_result = stats.ttest_ind(a=control_hit_ratios, b=test_hit_ratios, equal_var=True)
        print(
            f'## T-test result of [{each_q_strategy.strategy_name}] (sample_size={sample_size}, n_samples={n_samples})')

        print(f'- Avg hit ratio of ctrl strategy: {round(sum(control_hit_ratios) / len(control_hit_ratios), 3)}')
        print(f'- Avg hit ratio of test strategy: {round(sum(test_hit_ratios) / len(test_hit_ratios), 3)}')

        if t_test_result.pvalue < 0.05:
            print(f'- Result: REJECT null hypothesis (p-value: {t_test_result.pvalue})\n')
        else:
            print(f'- Result: ACCEPT null hypothesis (p-value: {t_test_result.pvalue})\n')


test_dataset_name = 'ml-1m'
test_repeating_times = 100000

# USER GUIDE: add the  questioning strategies to evaluate here
questioning_strategies = [questioning_random, questioning_favorite, questioning_rated_most, questioning_maniac]
# USER GUIDE: add the  matching strategies to evaluate here
matching_strategies = [matching_random]

# print_eval_result(test_dataset_name, test_repeating_times, questioning_strategies, matching_strategies)


## T-test
SAMPLE_SIZE = 100
N_SAMPLES = 200

print_t_test_result(test_dataset_name, questioning_strategies, SAMPLE_SIZE, N_SAMPLES)




