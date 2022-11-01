
class HierarchicalCluster:
    def __init__(self, ratings_df):
        self.ratings_df = ratings_df

        # depth is the level of the hierarchy
        # it is highly relevant with the number of questions to ask to users.
        # If the cluster has N depths, users will be asked N questions to match the user with a cluster
        self.depth = 0

    def get_depth(self):
        return self.depth

    def get_initial_cluster_num_by_elbow_method(self):
        return None


