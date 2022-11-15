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
    next_item = naive_item_selection_st.get_next_item(current_ratings)
    assert next_item in [1262, 1084]


def test_naive_item_selection_strategy_with_only_one_item_left_to_rate():
    naive_item_selection_st = s_naive('test1')
    current_ratings = "{'5618': '5.0', ' 1262': '1.0'}"
    next_item = naive_item_selection_st.get_next_item(current_ratings)
    assert next_item == 1084


def test_rated_by_most_st_has_the_most_ratings():
    rated_by_most_st = s_rated_most('test2')

    # select a random movie and add it as a movie which is already rated by an online user
    random_movie = choice(rated_by_most_st.clustering.rating_matrix.columns)

    # dummy input for get_next_item
    current_ratings_dict = {int(random_movie): 5.0}
    random_from_most_rated_movie_ids = rated_by_most_st.get_next_item(json.dumps(current_ratings_dict))

    # select the movie rated by the most
    original_input_data = pd.read_csv(raw_dataset_path(dataset_name='test2'))
    most_common_movies = Counter(original_input_data[ITEM_COL_NAME].to_list()).most_common(10)

    # column at index 0: movie IDs
    most_common_movie_ids = [each[0] for each in most_common_movies]

    assert random_from_most_rated_movie_ids in most_common_movie_ids

