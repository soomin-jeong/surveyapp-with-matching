from backend.src.strategies.next_question_selection.abstract_class.item_selection_base_choice import BaseStrategyChoice
from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from backend.src.strategies.preprocessing.hierarchical_clustering import UserCluster
from backend.src.strategies.next_question_selection.user_cluster_with_representative_item import UserClusterRep, \
    get_cluster_matched_up_to_now

from backend.src.utils.utils import convert_current_ratings_str_into_list


class Strategy(BaseStrategyChoice):
    strategy_name = 'rated_by_the_most'

    def __init__(self, dataset_name: str):
        super(Strategy, self).__init__(dataset_name)

    def add_representative_item_to_user_clusters_in_hc(self, curr_cluster: UserCluster):
        self.add_representative_items_to_children(curr_cluster)

        # TODO: add the comment why we go through loop here as an external layer of recursive function
        for each_child_cluster in curr_cluster.child_clusters:
            self.add_representative_item_to_user_clusters_in_hc(each_child_cluster)

        # if there are collisions among the representative items in child clusters
        # re-select the representative item to avoid the collision

    def add_representative_items_to_children(self, parent_cluster: UserCluster):
        child_clusters_with_rep_item = []
        for each_child in parent_cluster.child_clusters:
            # this strategy regards an item rated the most times by the users in the cluster as the representative item
            # therefore, when there is only one item, there is no item rated the most times,
            # because every item is rated once or not at all
            if each_child.user_cnt > 1:
                rep_item = self._get_representative_item_of_cluster(each_child)
                user_cluster_with_rep_item = UserClusterRep(each_child, rep_item)
                child_clusters_with_rep_item.append(user_cluster_with_rep_item)
            else:
                # though the clusters with only one user should not contain a representative item,
                # we are still adding it as we are overwriting the child clusters
                child_clusters_with_rep_item.append(each_child)

        parent_cluster.child_clusters = child_clusters_with_rep_item

    def has_next(self, choices_so_far_str: str) -> bool:
        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)
        curr_cluster = get_cluster_matched_up_to_now(self.clustering.root_cluster, choices_so_far)

        # if the curr_cluster has child clusters, it has items to return
        # else, it's the cluster with one user (like a leaf node in a tree)
        return curr_cluster.user_cnt > 2

    def _get_representative_item_of_cluster(self, cluster: UserCluster) -> int:

        # select item ratings by the users in each cluster in the data frame
        df_items_rated_by_the_cluster = self.clustering.rating_matrix.filter(items=cluster.user_ids, axis='rows')

        # if the representative items are redundant, replace it with the next level
        rating_cnt_per_item = df_items_rated_by_the_cluster.count()

        # sort it ascending and pick the last one
        return rating_cnt_per_item.sort_values().keys()[-1]

    def get_next_items(self, choices_so_far_str: str) -> [int]:
        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)
        # find the cluster that the user is matched depending on the choices up to now
        curr_cluster = get_cluster_matched_up_to_now(self.clustering.root_cluster, choices_so_far)

        if curr_cluster.user_cnt > 2:
            # return the representative items of the child clusters of the matched cluster up to now
            return [each_child.rep_item for each_child in curr_cluster.child_clusters]
        else:
            return []

    def simulate_online_user_response(self, online_user_id: int, candidate_item_ids: [int]) -> int:
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

        if highest_rated_item_id is None:
            return candidate_item_ids[0]

        return int(highest_rated_item_id)


