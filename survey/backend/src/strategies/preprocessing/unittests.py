import unittest

import pandas as pd
import numpy as np

from survey.backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from survey.backend.src.strategies.preprocessing.matrix_builder import MatrixBuilder

'''
+-----+------+---+------------+
| userId | movieId | rating | timestamp | 
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

SAMPLE_DATA = pd.read_csv('/Users/JeongSooMin/Documents/workspace/surveyapp-with-matching/survey/backend/data/datasets/movielens_small/ratings.csv')


DUMMY_RATINGS2 = pd.DataFrame(data=np.array([[459, 5618, 5, 1520233615],
                                             [477, 5618, 5, 1201159360],
                                             [298, 5618, 1, 1447598312],
                                             [219, 5618, 1, 1194685902],
                                             [459, 1262, 1, 1178293076],
                                             [477, 1262, 5, 1020802351],
                                             [298, 1084, 1, 1184619962],
                                             [219, 1084, 5, 974938169]]),
                              columns=['userId', 'movieId', 'rating', 'timestamp'])


DUMMY_RATINGS3 = pd.DataFrame(data=np.array([[459, 5618, 5, 1520233615],
                                             [477, 5618, 5, 1201159360],
                                             [412, 5618, 5, 1201159360],
                                             [298, 5618, 1, 1447598312],
                                             [297, 5618, 1, 1447598312],
                                             [219, 5618, 1, 1194685902],
                                             [459, 1262, 1, 1178293076],
                                             [477, 1262, 5, 1020802351],
                                             [412, 5618, 5, 1201159360],
                                             [298, 1084, 1, 1184619962],
                                             [297, 5618, 1, 1447598312],
                                             [219, 1084, 5, 974938169]]),
                              columns=['userId', 'movieId', 'rating', 'timestamp'])


class VectorizerTest(unittest.TestCase):
    vectorizer = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.vectorizer = MatrixBuilder(DUMMY_RATINGS2)
        cls.compressed_df = cls.vectorizer.rating_df

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
        print(TRANSPOSED_MATRIX)
        print(rating_matrix)
        assert TRANSPOSED_MATRIX.equals(rating_matrix)



class HierarchicalClusterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.hc2 = HierarchicalCluster(DUMMY_RATINGS2)
        cls.hc3 = HierarchicalCluster(DUMMY_RATINGS3)

    def test_HC_clusters_into_two_given_users_less_than_5(self):
        root_cluster = self.hc2.root_cluster
        assert len(root_cluster.child_clusters) == 2

    def test_HC_clusters_into_right_depth(self):
        assert self.hc2.depth == 2

    def test_HC_clusters_into_two_given_users_more_than_5(self):
        root_cluster = self.hc3.root_cluster
        assert len(root_cluster.child_clusters) == 3

    def test_root_cluster_contains_all_users(self):
        # using set instead of unique for sorting
        user_ids = self.hc2.rating_df['userId'].unique()
        user_ids.sort()
        assert self.hc2.root_cluster.user_ids == user_ids.tolist()

    def test_leaf_clusters_have_only_one_user(self):

        def find_leaf_clusters(curr_cluster, leaf_clusters):
            if not curr_cluster.child_clusters:
                leaf_clusters.append(curr_cluster)
            else:
                for each_child in curr_cluster.child_clusters:
                    find_leaf_clusters(each_child, leaf_clusters)

        leaf_clusters = []
        find_leaf_clusters(self.hc3.root_cluster, leaf_clusters)

        for each_leaf in leaf_clusters:
            if each_leaf.user_cnt != 1:
                self.fail("the leaf cluster does not have 1 user")


class HierarchicalClusterSampleDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hc4 = HierarchicalCluster(SAMPLE_DATA)

    def test_HC_clusters_sample_data_recursively_into_lte_7(self):
        assert len(self.hc4.root_cluster.child_clusters) < 8




