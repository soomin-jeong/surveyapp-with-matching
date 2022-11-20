import unittest

from backend.src.strategies.next_question_selection.implemented_strategies.rated_by_the_most_strategy import Strategy as s_rated_most
from backend.src.strategies.next_question_selection.implemented_strategies.random_selection_strategy import Strategy as s_naive
from backend.src.strategies.next_question_selection.implemented_strategies.favorite_item_strategy import Strategy as s_favorite

from backend.src.strategies.next_question_selection.user_cluster_with_representative_item import \
    get_cluster_matched_up_to_now

'''
the hierarchical clustering of 'TEST2'
level1: 219, 412, 297, 298, 459, 477
level2: 219, 412   // 297, 298, 459, 477
level3: 219 / 412  // 297, 298 / 459, 477
level3: -         /// 297 / 298 // 459 / 477
'''

class NaiveStrategyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.naive_item_selection_st = s_naive('test1')

    def test_naive_item_selection_strategy(self):
        current_ratings = "[5618]"
        next_items = self.naive_item_selection_st.get_next_items(current_ratings)
        assert 5618 not in next_items
        assert 1262 in next_items or 1084 in next_items


class RatedByMostStrategyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.rated_by_most_st = s_rated_most('test2')
        
    def test_rated_by_most_st_has_the_most_ratings(self):
        # the strategy should return [5618, 1084] as the items to choose from two clusters: [412, 219] [459, 477, 297, 298]
        assert self.rated_by_most_st.get_next_items("[]") == [5618, 1084] or \
               self.rated_by_most_st.get_next_items("[]") == [1084, 5618]
    
        # assume user chose 5618, matched with [459, 477, 297, 298] cluster
        # their child clusters [459, 477] [297, 298] both rated 5618  the most times (twice)
        assert self.rated_by_most_st.get_next_items("[5618]") == [5618, 5618]
    
        # user chose either [459, 477] or [297, 298], as both of their representative items are the same (5618)
        assert self.rated_by_most_st.get_next_items("[5618, 5618]") == []
    
        assert self.rated_by_most_st.has_next("[5618, 5618]") == False
    
    '''
    Assume a case where the user answered the last question,
    and there is no more items to choose from,
    because the user was already matched with a cluster with only one user in it
    '''
    def test_rated_by_most_st_returns_has_next_correctly(self):
    
        choices_till_the_last_level = "[5618, 5618]"
    
        # the strategy is expected to return empty list as the next items
        next_items = self.rated_by_most_st.get_next_items(choices_so_far_str=choices_till_the_last_level)
        assert next_items == []
    
        # the strategy is expected to show that it does not have next items to return any more
        assert self.rated_by_most_st.has_next(choices_till_the_last_level) is False
    
        # the matched current cluster is expected to have TWO users, with two clusters with one user in each
        # as this strategy should not reach the last level (one user in one cluster)
        # the matching will be decided by the matching strategy instead
        matched_curr = get_cluster_matched_up_to_now(self.rated_by_most_st.clustering.root_cluster,
                                                     [5618, 5618])
        assert len(matched_curr.child_clusters) == 2
        assert matched_curr.user_cnt == 2
    
    
    def test_rated_by_most_st_adds_representative_item_to_child_clusters(self):
        # test2 data set was designed so that clusters at each level does not contain any overlapping items rated
        # first child clusters: ['2: [219, 412]', '4: [297, 298, 459, 477]']
        # representative items (in the same order of child clusters): [1074,  5618]
    
        root_cluster = self.rated_by_most_st.clustering.root_cluster
        question_candidates_of_root = [each_child.rep_item for each_child in root_cluster.child_clusters]
        assert 5618 in question_candidates_of_root and \
            1084 in question_candidates_of_root and \
            len(question_candidates_of_root) == 2


class FavoriteItemStrategy(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.favorite_strategy = s_favorite('test2')

    def test_favorite_strategy_returns_favorite_item_of_cluster(self):
        root_cluster = self.favorite_strategy.clustering.root_cluster

        # favorite items of the fist level of hierarchy:
        # level2: 219, 412   // 297, 298, 459, 477
        # fav:    item 1084 //  item 5618
        question_candidates_of_root = [each_child.rep_item for each_child in root_cluster.child_clusters]
        assert 5618 in question_candidates_of_root and \
               1084 in question_candidates_of_root and \
               len(question_candidates_of_root) == 2
