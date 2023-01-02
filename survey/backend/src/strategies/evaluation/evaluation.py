import random
from backend.src.strategies.next_question_selection.abstract_class.item_selection_base_choice import BaseStrategyChoice \
    as QuestioningStrategyBase
from backend.src.strategies.matchmaking.abstract_class.matching_strategy_base import BaseStrategy as MatchingStrategyBase
from backend.src.strategies.next_question_selection.user_cluster_with_representative_item import \
    get_cluster_matched_up_to_now
from backend.src.utils.utils import convert_current_ratings_str_into_list


class EvaluationOfStrategies:
    def __init__(self, dataset_name: str, questioning_strategy: QuestioningStrategyBase, matching_strategy: MatchingStrategyBase):
        self.dataset_name = dataset_name
        self.questioning_strategy = questioning_strategy(dataset_name)
        self.matching_strategy = matching_strategy

    def _pick_online_user_id(self, user_cluster: UserCluster):
        return random.choice(user_cluster.user_ids)

    def _add_new_response_to_str(self, choices_so_far_str:str, new_response_item_id: int) -> str:
        # this function adds a new response into the string style list
        # add the new response:
        if choices_so_far_str == '[]':
            choices_so_far_list = [new_response_item_id]
        else:
            choices_so_far_list = choices_so_far_str[1:-1].split(',')
            choices_so_far_list.append(new_response_item_id)

        return "[{}]".format(','.join([str(each) for each in choices_so_far_list]))

    def find_offline_user_id_matching(self, online_user_id: int):

        qs = self.questioning_strategy

        choices_so_far_str = "[]"
        root_cluster = qs.clustering.root_cluster
        rating_matrix = qs.clustering.rating_matrix

        while qs.has_next(choices_so_far_str):
            next_items = qs.get_next_items(choices_so_far_str)
            if next_items == []:
                a = 1
            online_user_response_item_id = qs.simulate_online_user_response(online_user_id, next_items)
            choices_so_far_str = self._add_new_response_to_str(choices_so_far_str, online_user_response_item_id)

        choices_so_far = convert_current_ratings_str_into_list(choices_so_far_str)
        matched_cluster = get_cluster_matched_up_to_now(root_cluster, choices_so_far)
        matching_strategy = self.matching_strategy(matched_cluster=matched_cluster,
                                                   rating_matrix=rating_matrix,
                                                   online_user_rating=choices_so_far_str)

        return matching_strategy.get_matched_user_id_among_multiple_in_cluster()

    def get_hit_ratio_of_combination_of_questioning_and_matchmaking_strategy(self, repeating_times: int):
        hit_times = 0

        for n in range(repeating_times):
            online_user_id = self._pick_online_user_id(self.questioning_strategy.clustering.root_cluster)
            offline_user_id = self.find_offline_user_id_matching(online_user_id)
            if online_user_id == offline_user_id:
                hit_times += 1

        return hit_times / repeating_times


