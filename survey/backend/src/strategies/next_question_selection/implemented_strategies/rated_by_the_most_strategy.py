from backend.src.strategies.next_question_selection.abstract_class.item_selection_base import BaseStrategy
from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from backend.src.strategies.preprocessing.hierarchical_clustering import UserCluster

from backend.src.utils.utils import convert_current_ratings_str_into_list


class Strategy(BaseStrategy):
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.clustering = HierarchicalCluster(dataset_name)
        # group of item ids to ask as candidates to choose from at each question (in the order of questions)
        # self.question_candidates: [int] = self.get_question_candidates()

    def has_next(self, choices_so_far_str: str) -> bool:
        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)
        curr_cluster = self._get_cluster_matched_up_to_now(choices_so_far)

        # if the curr_cluster has child clusters, it has items to return
        # else, it's the cluster with one user (like a leaf node in a tree)
        if curr_cluster.child_clusters:
            return True
        else:
            return False

    def _get_representative_item_of_cluster(self, cluster: UserCluster) -> int:

        # select item ratings by the users in each cluster in the data frame
        df_items_rated_by_the_cluster = self.clustering.rating_matrix.filter(items=cluster.user_ids, axis='rows')

        # if the representative items are redundant, replace it with the next level
        rating_cnt_per_item = df_items_rated_by_the_cluster.count()

        # sort it ascending and pick the last one
        return rating_cnt_per_item.sort_values().keys()[-1]

    def add_representative_items_to_children(self, parent_cluster: UserCluster):
        for each_child in parent_cluster.child_clusters:
            each_child.rep_item = self._get_representative_item_of_cluster(each_child)

    def get_question_candidates(self, parent_cluster: UserCluster):
        question_candidates = []

        for each_child in parent_cluster.child_clusters:
            representative_item = self._get_representative_item_of_cluster(each_child)
            question_candidates.append(representative_item)

        return question_candidates

    def _get_cluster_matched_up_to_now(self, choices_so_far: [int]) -> UserCluster:
        curr_cluster = self.clustering.root_cluster

        for each_choice in choices_so_far:
            for each_child_cluster in curr_cluster.child_clusters:
                if each_choice == each_child_cluster.rep_item:
                    curr_cluster = each_child_cluster
                    break
        return curr_cluster

    def get_next_items(self, choices_so_far_str: str) -> [int]:
        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)

        # find the cluster that the user is matched depending on the choices up to now
        curr_cluster = self._get_cluster_matched_up_to_now(choices_so_far)
        self.add_representative_items_to_children(curr_cluster)

        # return the representative items of the child clusters of the matched cluster up to now
        return [each_child.rep_item for each_child in curr_cluster.child_clusters]


