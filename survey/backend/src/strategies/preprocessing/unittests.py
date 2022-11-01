import unittest

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


class VectorizerTest(unittest.TestCase):

    # using init instead of setUp because it will be shared by many tests
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vectorizer = Vectorizer(DUMMY_RATINGS2)
        self.compressed_df = self.vectorizer.rating_df

    # tests if the data frame from the `ratings.csv` is successfully transposed so that the columns are the items
    def test_transpose_to_rating_matrix(self):
        rating_matrix = self.vectorizer.rating_matrix

        # user_id, item 5618, item 1262, item 1084, timestamp
        TRANSPOSED_MATRIX = pd.DataFrame(data=np.array(pd.DataFrame(data=np.array([[5, None, 1],
                                                                                   [1, None, 1],
                                                                                   [None, 1, 5],
                                                                                   [None, 5, 5]]))))
        TRANSPOSED_MATRIX = TRANSPOSED_MATRIX.rename(index={0: 219, 1: 298, 2: 459, 3: 477},
                                                     columns={0: 1084, 1: 1262, 2: 5618})

        assert TRANSPOSED_MATRIX.equals(rating_matrix)


class HierarchicalClusterTest(unittest.TestCase):
    def __init__(self):
        super().__init__()
        self.hc = HierarchicalCluster(DUMMY_RATINGS2)

    def test_hierarchical_clustering_classifies_upto_expected_depth(self):
        assert self.hc.get_depth() == 3


