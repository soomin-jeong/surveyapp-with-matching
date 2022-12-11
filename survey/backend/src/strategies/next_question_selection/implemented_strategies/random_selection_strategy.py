import random

from backend.src.strategies.next_question_selection.abstract_class.item_selection_base_choice import BaseStrategyChoice
from backend.src.strategies.preprocessing.hierarchical_clustering import UserCluster
from backend.src.strategies.next_question_selection.user_cluster_with_representative_item import UserClusterRep, \
    get_cluster_matched_up_to_now

from backend.src.utils.utils import convert_current_ratings_str_into_list


class Strategy(BaseStrategyChoice):
    strategy_name = 'random_item'

    def has_next(self, choices_so_far_str: str) -> bool:
        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)
        return len(choices_so_far) < self.clustering.rating_matrix_na_filled.columns

    def add_representative_items_to_children(self, parent_cluster: UserCluster):
        child_clusters_with_rep_item = []
        for each_child in parent_cluster.child_clusters:
            rep_item = self._get_representative_item_of_cluster(each_child)
            user_cluster_with_rep_item = UserClusterRep(each_child, rep_item)
            child_clusters_with_rep_item.append(user_cluster_with_rep_item)
        parent_cluster.child_clusters = child_clusters_with_rep_item

    def _get_representative_item_of_cluster(self, cluster: UserCluster) -> int:
        df_items_rated_by_the_cluster = self.clustering.rating_matrix.filter(items=cluster.user_ids, axis='rows')
        random_item_rated = random.choice(df_items_rated_by_the_cluster.columns)
        return random_item_rated

    def get_next_items(self, choices_so_far_str: str) -> [int]:
        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)
        # find the cluster that the user is matched depending on the choices up to now
        curr_cluster = get_cluster_matched_up_to_now(self.clustering.root_cluster, choices_so_far)

        if curr_cluster.user_cnt > 1:
            # return the representative items of the child clusters of the matched cluster up to now
            return [each_child.rep_item for each_child in curr_cluster.child_clusters]
        else:
            return []

    def simulate_online_user_response(self, online_user_id: int, candidate_item_ids: [int]) -> int:
        return random.choice(candidate_item_ids)



