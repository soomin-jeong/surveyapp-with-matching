import pandas as pd
import numpy as np

from survey.backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from survey.backend.src.strategies.preprocessing.vectorizer import Vectorizer

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


def test_hierarchical_clustering_classifies_upto_expected_depth():
    hc = HierarchicalCluster(DUMMY_RATINGS2)
    assert hc.get_depth() == 3


def test_if_compressing_user_ids_and_movie_ids_leaves_only_unique_ids():
    vectorizer = Vectorizer(DUMMY_RATINGS2)
    vectorizer.compress_sparse_ids()
    compressed_df = vectorizer.rating_df

    # as they are compressed, ID of the last user should be the number of unique users
    last_user = compressed_df['user'].max()
    last_movie = compressed_df['movie'].max()

    # +1 as the IDs start from 0
    assert last_user + 1 == len(DUMMY_RATINGS2['userId'].unique())
    assert last_movie + 1 == len(DUMMY_RATINGS2['movieId'].unique())


# tests if the data frame from the `ratings.csv` is successfully transposed so that the columns are the items
def test_transpose_to_rating_matrix():
    DUMMY_RATINGS2 = pd.DataFrame(data=np.array([[459, 5618, 5, 1520233615],
                                                 [477, 5618, 5, 1201159360],
                                                 [298, 5618, 1, 1447598312],
                                                 [219, 5618, 1, 1194685902],
                                                 [459, 1262, 1, 1178293076],
                                                 [477, 1262, 5, 1020802351],
                                                 [298, 1084, 1, 1184619962],
                                                 [219, 1084, 5, 974938169]]),
                                 columns=['userId', 'movieId', 'rating', 'timestamp'])

    vectorizer = Vectorizer(DUMMY_RATINGS2)
    rating_matrix = vectorizer.vectorize()

    # user_id, item 5618, item 1262, item 1084, timestamp
    TRANSPOSED_MATRIX = pd.DataFrame(data=np.array(pd.DataFrame(data=np.array([[459, 5, 1, None, 1520233615],
                                                                               [477, 5, 5, None, 1201159360],
                                                                               [476, 5, 4, None, 1201159360],
                                                                               [298, 1, None, 1, 1447598312],
                                                                               [219, 1, None, 5, 1194685902]]))))
    assert rating_matrix == TRANSPOSED_MATRIX