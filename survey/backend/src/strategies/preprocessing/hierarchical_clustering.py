import os
import pandas as pd
import pickle

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from backend.src.strategies.preprocessing.matrix_builder import MatrixBuilder

# the number of candidates (options) at questions for the online users
# for example, if this var is 5, users will see at most 5 options to choose among at each question.
from backend.src.strategies.preprocessing.utils import clustered_result_path, raw_dataset_path


MAXIMUM_CANDIDATES = 5


def depth(l):
    if isinstance(l, list):
        return 1 + max(depth(item) for item in l)
    else:
        return 0


class HierarchicalCluster:
    class UserCluster:
        def __init__(self, is_root=False):
            self.is_root: bool = is_root
            self.parent_cluster = None
            self.child_clusters = []
            self.user_ids: [int] = []
            self.user_cnt: int = 0

        def __repr__(self):
            return repr(f'{self.user_cnt}: {self.user_ids}')

    def __init__(self, dataset_name: str):
        self.depth: int = 0

        if os.path.exists(clustered_result_path(dataset_name)):

            with open(clustered_result_path(dataset_name), 'rb') as cluster_file_r:
                temp_hc = pickle.load(cluster_file_r)
                self.root_cluster = temp_hc.root_cluster
                self.rating_matrix = temp_hc.rating_matrix
        else:
            rating_df = pd.read_csv(raw_dataset_path(dataset_name))
            self.rating_matrix = self.preprocess_input_df(rating_df)
            self.root_cluster = self.cluster_users_by_rating()

            # depth is the level of the hierarchy
            # it is highly relevant with the number of questions to ask to users.
            # If the cluster has N depths, users will be asked N questions to match the user with a cluster
            self.depth = 1 + depth(self.root_cluster.child_clusters)

            # save the class into the CLUSTERED_RESULT_PATH
            dir = '/'.join(clustered_result_path(dataset_name).split('/')[:-1])
            if not os.path.exists(dir):
                os.makedirs(dir)

            with open(clustered_result_path(dataset_name), 'wb') as cluster_file_w:
                pickle.dump(self, cluster_file_w)

    def preprocess_input_df(self, rating_df):
        matrix_builder = MatrixBuilder(rating_df)
        rating_matrix = matrix_builder.rating_matrix

        # TODO: consider other options for the fillna
        # filling the missing data with the column-wise (item-wise) average rating of the item
        return rating_matrix.fillna(rating_matrix.mean(), axis=0)

    def cluster_users_by_rating(self):
        root_cluster = self.UserCluster(is_root=True)
        root_cluster.user_ids = self.rating_matrix.index.to_list()
        root_cluster.user_cnt = len(root_cluster.user_ids)

        # if you'd like to use elbow method, not using the default value 5 for the clustering,
        # set the `elbow_method` argument as True
        # i.e. self.build_child_clusters(root_cluster, True)
        self.build_child_clusters(root_cluster)
        return root_cluster

    def build_child_clusters(self, curr_cluster: UserCluster, elbow_method: bool = False):

        # run k-means clusters based on elbow method
        curr_rating_matrix = self.rating_matrix.loc[curr_cluster.user_ids]
        unique_user_cnt = curr_rating_matrix.shape[0]

        # assign the current cluster(self) as the parent cluster to the child clusters
        # handling exceptional cases where the users are too few
        if unique_user_cnt <= 5:

            kmeanModel = KMeans(n_clusters=2)
            kmeanModel.fit(curr_rating_matrix)
            best_k_means = kmeanModel

        else:
            if elbow_method:
                # find the desirable number of clusters
                # limiting between 2 to smaller number between (total number of unique users - 1) / 2 or 7
                # as too many clusters make it harder to choose an option among them
                K = range(1, min(int(unique_user_cnt / 2) + 1, MAXIMUM_CANDIDATES + 1))

                kmeanModels = []
                inertias = []

                for k in K:
                    kmeanModel = KMeans(n_clusters=k)
                    kmeanModel.fit(curr_rating_matrix)

                    # keeping the current model until we know the desirable k
                    kmeanModels.append(kmeanModel)

                    # Inertia is the sum of the squared distances of *samples* to their closest cluster center
                    inertia = kmeanModel.inertia_
                    inertias.append(inertia)

                desirable_k = None

                # we look for the *elbow* here
                # elbow is the number of clusters
                # where the linearly decreasing inertia starts to decrease slower than the previous numbers
                for idx in range(0, len(inertias)):
                    # excluding 1 cluster at idx 0 because 1 will make the hierarchical clustering infinite
                    if idx == 0:
                        pass
                    # if there's no elbow at last, return the last idx
                    elif idx == len(inertias) - 1:
                        desirable_k = idx + 1
                    elif inertias[idx - 1] - inertias[idx] > inertias[idx] - inertias[idx + 1]:
                        desirable_k = idx + 1

                best_k_means = kmeanModels[desirable_k - 1]

            else:
                best_k_means = KMeans(n_clusters=MAXIMUM_CANDIDATES)
                best_k_means.fit(curr_rating_matrix)

        curr_rating_matrix['labels'] = best_k_means.labels_

        # for each child cluster, assign the parent cluster and user_ids
        for each_label in range(best_k_means.n_clusters):
            child_rating_matrix = curr_rating_matrix[curr_rating_matrix['labels'] == each_label]
            child = self.UserCluster()
            child.user_ids = child_rating_matrix.index.to_list()
            child.user_cnt = len(child.user_ids)
            child.parent_cluster = curr_cluster

            curr_cluster.child_clusters.append(child)

        for each_child in curr_cluster.child_clusters:
            if len(each_child.user_ids) > 1:
                self.build_child_clusters(curr_cluster=each_child)
