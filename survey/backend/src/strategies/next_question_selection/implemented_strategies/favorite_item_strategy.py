import os

from backend.src.strategies.next_question_selection.abstract_class.item_selection_base_choice import BaseStrategyChoice
from backend.src.utils.utils import convert_current_ratings_str_into_list

from backend.src.strategies.preprocessing.hierarchical_clustering import UserCluster
from backend.src.strategies.next_question_selection.user_cluster_with_representative_item import UserClusterRep, \
    get_cluster_matched_up_to_now


class Strategy(BaseStrategyChoice):
    strategy_name = 'favorite_item'

    def __init__(self, dataset_name: str):
        super(Strategy, self).__init__(dataset_name)

    def add_representative_item_to_user_clusters_in_hc(self, curr_cluster: UserCluster):
        self.add_representative_items_to_children(curr_cluster)
        for each_child_cluster in curr_cluster.child_clusters:
            self.add_representative_item_to_user_clusters_in_hc(each_child_cluster)

    def add_representative_items_to_children(self, parent_cluster: UserCluster):
        child_clusters_with_rep_item = []
        for each_child in parent_cluster.child_clusters:
            # this strategy regards an item with the highest average rating as representative item
            rep_item = self._get_representative_item_of_cluster(each_child)
            user_cluster_with_rep_item = UserClusterRep(each_child, rep_item)
            child_clusters_with_rep_item.append(user_cluster_with_rep_item)
        parent_cluster.child_clusters = child_clusters_with_rep_item

    def _get_representative_item_of_cluster(self, cluster: UserCluster) -> int:

        # select item ratings by the users in each cluster in the data frame
        df_items_rated_by_the_cluster = self.clustering.rating_matrix.filter(items=cluster.user_ids, axis='rows')
        average_rating_per_item = df_items_rated_by_the_cluster.mean(axis='rows')

        # sort it descending and pick the first one
        return average_rating_per_item.sort_values(ascending=False).keys()[0]

    def has_next(self, choices_so_far_str: str) -> bool:
        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)
        curr_cluster = get_cluster_matched_up_to_now(self.clustering.root_cluster, choices_so_far)

        # we can expect next item until we reach the cluster with only one user
        return curr_cluster.user_cnt > 1

    def get_next_items(self, choices_so_far_str: str) -> [int]:
        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)
        # find the cluster that the user is matched depending on the choices up to now
        curr_cluster = get_cluster_matched_up_to_now(self.clustering.root_cluster, choices_so_far)

        if curr_cluster.user_cnt > 1:
            # return the representative items of the child clusters of the matched cluster up to now
            return [each_child.rep_item for each_child in curr_cluster.child_clusters]
        else:
            return []

    def simulate_online_user_response(self, online_user_id: int, candidate_item_ids: [int]):
        # if there is no item or only one item
        if len(candidate_item_ids) <= 1:
            raise Exception('There should be at least 2 items in `candidate_item_ids` for this method')

        ratings_by_online_user = self.clustering.rating_matrix.loc[[online_user_id]]

        # giving the default value as low as possible
        highest_rated_item_id = None
        highest_rating_so_far = - float('inf')

        # pick the item with highest rating by an online user
        for each_item_id in candidate_item_ids:
            rating = ratings_by_online_user[each_item_id].values[0]
            if rating and rating > highest_rating_so_far:
               highest_rated_item_id = each_item_id

        return int(highest_rated_item_id)



    


