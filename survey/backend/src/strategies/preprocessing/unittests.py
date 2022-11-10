import unittest
import os

import pandas as pd
import numpy as np

import pickle

from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from backend.src.strategies.preprocessing.matrix_builder import MatrixBuilder
from backend.src.strategies.preprocessing.utils import clustered_result_path
from backend.src.strategies.preprocessing.utils import raw_dataset_path

from backend.src.strategies.preprocessing.hierarchical_clustering import MAXIMUM_CANDIDATES

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

DATASET_PATH = '../../../data/datasets/'

TEST1_DATASET_NAME = 'test1'
DUMMY_RATINGS2 = pd.read_csv(raw_dataset_path(TEST1_DATASET_NAME))

TEST2_DATASET_NAME = 'test2'
DUMMY_RATINGS3 = pd.read_csv(raw_dataset_path(TEST2_DATASET_NAME))

SAMPLE_DATASET_PATH = 'movielens_small'
SAMPLE_DATA = pd.read_csv(raw_dataset_path(SAMPLE_DATASET_PATH))


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
        assert TRANSPOSED_MATRIX.equals(rating_matrix)


class HierarchicalClusterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # in order to test new datasets and old ones,
        # we leave the clustered results of only TEST1_DATASET_NAME,
        # as if TEST2_DATASET_NAME is the new dataset.
        cls.hc1 = HierarchicalCluster(TEST1_DATASET_NAME)
        cls.addClassCleanup(os.remove, clustered_result_path(TEST1_DATASET_NAME))
        cls.hc2 = HierarchicalCluster(TEST2_DATASET_NAME)

    def test_HC_clusters_into_two_given_users_less_than_5(self):
        root_cluster = self.hc1.root_cluster
        assert len(root_cluster.child_clusters) == 2

    def test_HC_clusters_into_right_depth(self):
        assert self.hc1.depth == 2

    def test_HC_clusters_into_two_given_users_more_than_5(self):
        root_cluster = self.hc2.root_cluster
        assert len(root_cluster.child_clusters) == 3

    def test_root_cluster_contains_all_users(self):
        # using set instead of unique for sorting
        user_ids = self.hc1.rating_df['userId'].unique()
        user_ids.sort()
        assert self.hc1.root_cluster.user_ids == user_ids.tolist()

    def test_leaf_clusters_have_only_one_user(self):

        def find_leaf_clusters(curr_cluster, leaf_clusters):
            if not curr_cluster.child_clusters:
                leaf_clusters.append(curr_cluster)
            else:
                for each_child in curr_cluster.child_clusters:
                    find_leaf_clusters(each_child, leaf_clusters)

        leaf_clusters = []
        find_leaf_clusters(self.hc2.root_cluster, leaf_clusters)

        for each_leaf in leaf_clusters:
            if each_leaf.user_cnt != 1:
                self.fail("the leaf cluster does not have 1 user")

    def test_clustered_result_is_saved_at_correct_path(self):
        assert os.path.exists(clustered_result_path(TEST1_DATASET_NAME))
        assert os.path.exists(clustered_result_path(TEST2_DATASET_NAME))

    def test_clustered_result_is_saved(self):
        with open(clustered_result_path(TEST1_DATASET_NAME), 'rb') as cluster_file:
            temp_hc = pickle.load(cluster_file)
            assert self.hc1.rating_matrix.equals(temp_hc.rating_matrix)
            assert len(self.hc1.root_cluster.child_clusters) == len(temp_hc.root_cluster.child_clusters)


class HierarchicalClusterSampleDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hc4 = HierarchicalCluster(SAMPLE_DATASET_PATH)

    def test_HC_clusters_sample_data_recursively_into_lte_7(self):
        assert len(self.hc4.root_cluster.child_clusters) <= MAXIMUM_CANDIDATES




