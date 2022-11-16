import pandas as pd
import json
import numpy as np

from collections import Counter
from random import choice
from backend.src.strategies.next_question_selection.implemented_strategies.rated_by_the_most_strategy import Strategy as s_rated_most
from backend.src.strategies.next_question_selection.implemented_strategies.naive_item_selection_strategy import Strategy as s_naive

from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from backend.src.strategies.preprocessing.utils import raw_dataset_path
from backend.settings import ITEM_COL_NAME


DUMMY_RATINGS = pd.DataFrame(data=np.array([['459', '5618', '5.0', '1520233615'],
                                            ['477', '5618', '4.0', '1201159360'],
                                            ['298', '5618', '2.5', '1447598312'],
                                            ['219', '1262', '3.5', '1194685902'],
                                            ['483', '1262', '3.5', '1178293076'],
                                            ['45', '1262', '5.0', '1020802351'],
                                            ['606', '1262', '3.5', '1184619962'],
                                            ['290', '1084', '5.0', '974938169'],
                                            ['445', '6016', '2.0', '1454621781'],
                                            ['455', '440', '3.0', '836436201']]),
                             columns=['userId', 'movieId', 'rating', 'timestamp'])


'''
+-----+------+---+------------+
| 459 | 5618 | 5 | 1520233615 |
+-----+------+---+------------+
| 477 | 5618 | 5 | 1201159360 |
+-----+------+---+------------+
| 298 | 5618 | 1 | 1447598312 |
+-----+------+---+------------+
| 219 | 5618 | 1 | 1194685902 |
+-----+------+---+------------+
| 459 | 1262 | 1 | 1178293076 |
+-----+------+---+------------+
| 477 | 1262 | 5 | 1020802351 |
+-----+------+---+------------+
| 298 | 1084 | 1 | 1184619962 |
+-----+------+---+------------+
| 219 | 1084 | 5 | 974938169  |
+-----+------+---+------------+
Expected to be clustered: (((459), (477)), ((298), (219)))
'''


DUMMY_RATINGS2 = pd.DataFrame(data=np.array([[459, 5618, 5, 1520233615],
                                             [477, 5618, 5, 1201159360],
                                             [298, 5618, 1, 1447598312],
                                             [219, 5618, 1, 1194685902],
                                             [459, 1262, 1, 1178293076],
                                             [477, 1262, 5, 1020802351],
                                             [298, 1084, 1, 1184619962],
                                             [219, 1084, 5, 974938169]]),
                              columns=['userId', 'movieId', 'rating', 'timestamp'])


def test_naive_item_selection_strategy():
    hc1 = HierarchicalCluster('test1')
    naive_item_selection_st = s_naive(hc1)
    current_ratings = "{'5618': '5.0'}"
    next_item = naive_item_selection_st.get_next_items(current_ratings)
    assert next_item in [1262, 1084]


def test_naive_item_selection_strategy_with_only_one_item_left_to_rate():
    naive_item_selection_st = s_naive('test1')
    current_ratings = "{'5618': '5.0', ' 1262': '1.0'}"
    next_item = naive_item_selection_st.get_next_items(current_ratings)
    assert next_item == 1084


'''
hierachical clustering of 'test2' dataset:
[219, 297, 298, 412, 459, 477]
[412, 459, 477, 219]    [297, 298]
[412, 459, 219] [477]   [297] [298]
[412, 459] [219] [477]  [297] [298]
[412] [459] [219] [477] [297] [298]

459: 5618, 1262
477: 5618, 1262
412: 5618, 1084
298: 5618, 1984
297: 5618, 1262
219: 5618, 1984

1st question: 1262, 1984 (choose 1262)
2nd question: 1262, 1084 (choose 1084)
match with 412
'''
def test_rated_by_most_st_has_the_most_ratings():
    rated_by_most_st = s_rated_most('test2')

    # the strategy should return 1262 and 1984 as the items to choose from two clusters: [412, 459, 477] [219, 297, 298]
    assert rated_by_most_st.get_next_items("[]") == [1262, 1984]

    # assume user chose 1262, matched with [412, 459, 477] cluster
    # the strategy should return 1262 and 1984 as the items to choose from two clusters: [412, 459] [477]
    assert rated_by_most_st.get_next_items("[1262]") == [1262, 1084]

    # assume user chose 1084, matched with [412] cluster
    # now that the user was matched with a cluster with only one user (id: 412), the `get_next_items` return an empty list
    assert rated_by_most_st.get_next_items("[1262, 1084]") == []



def test_skipping_to_next_question_if_prev_answer_already_matches_with_cluster():
    pass
