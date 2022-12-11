import random

from backend.src.strategies.next_question_selection.implemented_strategies.favorite_item_strategy import \
            Strategy as questioning_favorite
from backend.src.strategies.matchmaking.implemented_strategies.random_matchmaking_strategy import \
            Strategy as matchmaking_random

from backend.src.strategies.next_question_selection.user_cluster_with_representative_item import \
    get_cluster_matched_up_to_now

from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster, UserCluster
from backend.src.utils.utils import convert_current_ratings_str_into_list


class EvaluationOfStrategies:
    def __init__(self, n_times: int, dataset_name: str):
        self.dataset_name = dataset_name
        self.n_times = n_times

    def _pick_online_user_id(self, user_cluster: UserCluster):
        return random.choice(user_cluster.user_ids)

    def find_offline_user_id_matching(self, online_user_id: int):
        h_clustering = HierarchicalCluster(self.dataset_name)
        root_cluster = h_clustering.root_cluster

        questioning_strategy = questioning_favorite(self.dataset_name)

        choices_so_far_str = "[]"

        while questioning_strategy.has_next(choices_so_far_str):
            next_items = questioning_strategy.get_next_items(choices_so_far_str)
            online_user_response_item_id = questioning_strategy.simulate_online_user_response(online_user_id, next_items)

            # add the new response:
            if choices_so_far_str == '[]':
                choices_so_far_list = [online_user_response_item_id]
            else:
                choices_so_far_list = choices_so_far_str[1:-1].split(',')
                choices_so_far_list.append(online_user_response_item_id)

            choices_so_far_str = "[{}]".format(','.join([str(each) for each in choices_so_far_list]))

        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)
        matched_cluster = get_cluster_matched_up_to_now(root_cluster, choices_so_far)
        matching_strategy = matchmaking_random(matched_cluster=matched_cluster,
                                               rating_matrix=h_clustering.rating_matrix,
                                               online_user_rating=choices_so_far_str)

        return matching_strategy.get_matched_user_id_among_multiple_in_cluster()

    def get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy(self):
        hit_times = 0

        for n in range(self.n_times):

            h_clustering = HierarchicalCluster(self.dataset_name)
            root_cluster = h_clustering.root_cluster

            online_user_id = self._pick_online_user_id(root_cluster)
            offline_user_id = self.find_offline_user_id_matching(online_user_id)
            if online_user_id == offline_user_id:
                hit_times += 1

        return hit_times / self.n_times


ev = EvaluationOfStrategies(100, 'movielens_small')
print(ev.get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy())