from backend.src.strategies.preprocessing.hierarchical_clustering import UserCluster

# this class is inheriting user cluster class and adding one element, representative item
# inheritance was chosen because representative item only exists under a combination of a user cluster AND a strategy

# this class simply gets a representative item as an input, allowing it to be decided out of this class,
# because the representative item may depend on the items of other user clusters in the same level of hierarchy
# (i.e. rated_by_the_most_strategy)


class UserClusterRep(UserCluster):
    def __init__(self, user_cluster: UserCluster, rep_item: int):
        super(UserClusterRep, self).__init__(is_root=user_cluster.is_root)
        # inheriting the existing elements
        self.child_clusters = user_cluster.child_clusters
        self.is_root = user_cluster.is_root
        self.parent_cluster = user_cluster.parent_cluster
        self.user_cnt = user_cluster.user_cnt
        self.user_ids = user_cluster.user_ids

        # adding a new attribute, representative item of this cluster
        self.rep_item = rep_item

    def __repr__(self):
        return repr(f'users: {self.user_ids} / rep: {self.rep_item}')


def get_cluster_matched_up_to_now(root_cluster: UserCluster, choices_so_far: [int]) -> UserCluster:
    curr_cluster = root_cluster

    for each_choice in choices_so_far:
        for each_child_cluster in curr_cluster.child_clusters:
            if each_choice == each_child_cluster.rep_item:
                curr_cluster = each_child_cluster
                break
    return curr_cluster