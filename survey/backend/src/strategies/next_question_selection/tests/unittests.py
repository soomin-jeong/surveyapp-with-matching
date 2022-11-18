import pandas as pd
import json
import numpy as np

from collections import Counter
from random import choice
from backend.src.strategies.next_question_selection.implemented_strategies.rated_by_the_most_strategy import Strategy as s_rated_most
from backend.src.strategies.next_question_selection.implemented_strategies.naive_item_selection_strategy import Strategy as s_naive

from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from backend.src.utils.utils import raw_dataset_path
from backend.settings import ITEM_COL_NAME


def test_naive_item_selection_strategy():
    naive_item_selection_st = s_naive('test1')
    current_ratings = "[5618]"
    next_items = naive_item_selection_st.get_next_items(current_ratings)
    assert 5618 not in next_items
    assert 1262 in next_items or 1084 in next_items


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

    # the strategy should return [5618, 1084] as the items to choose from two clusters: [412, 219] [459, 477, 297, 298]
    assert rated_by_most_st.get_next_items("[]") == [5618, 1084] or \
           rated_by_most_st.get_next_items("[]") == [1084, 5618]

    # assume user chose 5618, matched with [459, 477, 297, 298] cluster
    # their child clusters [459, 477] [297, 298] both rated 5618  the most times (twice)
    assert rated_by_most_st.get_next_items("[5618]") == [5618, 5618]


def test_rated_by_most_st_adds_representative_item_to_child_clusters():
    # test2 data set was designed so that clusters at each level does not contain any overlapping items rated
    # first child clusters: ['2: [219, 412]', '4: [297, 298, 459, 477]']
    # representative items (in the same order of child clusters): [1074,  5618]

    rated_by_most_st = s_rated_most('test2')
    root_cluster = rated_by_most_st.clustering.root_cluster
    rated_by_most_st.add_representative_items_to_children(root_cluster)
    question_candidates_of_root = [each_child.rep_item for each_child in root_cluster.child_clusters]
    assert 5618 in question_candidates_of_root and \
        1084 in question_candidates_of_root and \
        len(question_candidates_of_root) == 2
