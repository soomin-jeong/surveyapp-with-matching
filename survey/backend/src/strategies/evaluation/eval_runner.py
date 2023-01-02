import time

import numpy as np
import statistics

import scipy.stats as stats
import matplotlib.pyplot as plt

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
            print("Hit Rate (questioning={}, matching={}): \t{} (in {}s)\n".format(each_questioning_strategy.strategy_name,
                                                                                 each_matching_strategy.strategy_name,
                                                                                 hit_ratio,
                                                                                 round(end-start, 5)))



def print_t_test_result(dataset_name, matching_strategies, questioning_strategies, sample_size, n_samples):
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

    CONTROL_MATCHING_STRATEGY = matching_random
    CONTROL_QUESTIONING_STRATEGY = questioning_random

    control_hit_ratios = collect_hit_ratio(dataset_name, CONTROL_QUESTIONING_STRATEGY,
                                           CONTROL_MATCHING_STRATEGY, sample_size, n_samples)

    print("1: NORMALITY")
    control_normality = stats.shapiro(control_hit_ratios)
    print(f'[{CONTROL_MATCHING_STRATEGY.strategy_name}] normal dist p-val: {control_normality.pvalue}')

    plt.hist(control_hit_ratios, 10)
    plt.title(
        f'[q={CONTROL_QUESTIONING_STRATEGY.strategy_name}, m={CONTROL_MATCHING_STRATEGY.strategy_name}]\n (sample_size={sample_size}, n_samples={n_samples})')
    plt.show()

    for each_m_strategy in matching_strategies:
        for each_q_strategy in questioning_strategies:
            test_hit_ratios = collect_hit_ratio(dataset_name, each_q_strategy, each_m_strategy, sample_size, n_samples)

            # Testing Normality
            test_normality = stats.shapiro(test_hit_ratios)
            print(f'[{each_q_strategy.strategy_name}] normal dist p-val: {test_normality.pvalue}')

            if control_normality.pvalue >= 0.05:
                print(f'✅ [{CONTROL_QUESTIONING_STRATEGY.strategy_name}] is normally distributed')
            else:
                print(f'❌ [{CONTROL_QUESTIONING_STRATEGY.strategy_name}] is NOT normally distributed')

            if test_normality.pvalue >= 0.05:
                print(f'✅ [{each_q_strategy.strategy_name}] is normally distributed')
            else:
                print(f'❌ [{each_q_strategy.strategy_name}] is NOT normally distributed')
            print('\n')

            plt.hist(test_hit_ratios, 10)
            plt.title(f'[q={each_q_strategy.strategy_name}, m={each_m_strategy.strategy_name}] (sample_size={sample_size}, n_samples={n_samples})')
            plt.show()

            # Testing Variance
            print("2: VARIANCE")

            print(f'[{CONTROL_MATCHING_STRATEGY.strategy_name}] variance: {statistics.variance(control_hit_ratios)}')
            print(f'[{each_q_strategy.strategy_name}] variance: {statistics.variance(test_hit_ratios)}')

            var_comparison = stats.levene(control_hit_ratios, test_hit_ratios, center='mean').pvalue
            equal_var = (var_comparison >= 0.05)
            if equal_var:
                print(f'✅ Variances are similar (pval < 0.05)')
            else:
                print(f'❌ Variances are NOT similar (pval >= 0.05)')
            print('\n')

            # Hypothesis Test 1
            ranksum_test = stats.ranksums(control_hit_ratios, test_hit_ratios)

            print(
                f'3. RankSum result of [q={each_q_strategy.strategy_name}, m={each_m_strategy.strategy_name}] (sample_size={sample_size}, n_samples={n_samples})')

            print(f'- Avg hit ratio of ctrl strategy: {round(sum(control_hit_ratios) / len(control_hit_ratios), 3)}')
            print(f'- Avg hit ratio of test strategy: {round(sum(test_hit_ratios) / len(test_hit_ratios), 3)}')

            if ranksum_test.pvalue < 0.05:
                print(f'- ✅ Result: REJECT null hypothesis (p-value: {ranksum_test.pvalue})')
            else:
                print(f'- ❌ Result: ACCEPT null hypothesis (p-value: {ranksum_test.pvalue})')
            print('\n')


            # Hypothesis Test 2
            t_test_result = stats.ttest_ind(a=control_hit_ratios, b=test_hit_ratios, equal_var=equal_var)
            print(
                f'4. T-test result of [q={each_q_strategy.strategy_name}, m={each_m_strategy.strategy_name}] (sample_size={sample_size}, n_samples={n_samples})')

            print(f'- Avg hit ratio of ctrl strategy: {round(sum(control_hit_ratios) / len(control_hit_ratios), 3)}')
            print(f'- Avg hit ratio of test strategy: {round(sum(test_hit_ratios) / len(test_hit_ratios), 3)}')

            if t_test_result.pvalue < 0.05:
                print(f'- ✅ Result: REJECT null hypothesis (p-value: {t_test_result.pvalue})')
            else:
                print(f'- ❌ Result: ACCEPT null hypothesis (p-value: {t_test_result.pvalue})')
            print('\n')


test_dataset_name = 'movielens_small'
test_repeating_times = 100

# USER GUIDE: add the  questioning strategies to evaluate here
questioning_strategies = [questioning_favorite, questioning_rated_most, questioning_maniac]
# USER GUIDE: add the  matching strategies to evaluate here
matching_strategies = [matching_random, matching_least_diff]

# print_eval_result(test_dataset_name, test_repeating_times, questioning_strategies, matching_strategies)


## T-test
# SAMPLE_SIZE = 5500
# N_SAMPLES = 100
# test_dataset_names = ['movielens_small', 'ml-100k', 'ml-1m']


print_t_test_result('movielens_small', [matching_random], [questioning_random], 5500, 100)
print_t_test_result('ml-100k', [matching_random], [questioning_random], 7500, 100)
print_t_test_result('ml-1m', [matching_random], [questioning_random], 80000, 100)




