
from sklearn.cluster import KMeans
from survey.backend.src.strategies.preprocessing.matrix_builder import MatrixBuilder


class HierarchicalCluster:
    def __init__(self, ratings_df):
        self.ratings_df = ratings_df

        # depth is the level of the hierarchy
        # it is highly relevant with the number of questions to ask to users.
        # If the cluster has N depths, users will be asked N questions to match the user with a cluster
        self.depth = 0
        self.cluster_labels = []

    # elbow method provides a desirable number of clusters for k-means clustering
    def get_desriable_cluster_num_with_elbow_method(self, curr_ratings_df):
        matrix_builder = MatrixBuilder(curr_ratings_df)
        rating_matrix = matrix_builder.rating_matrix

        # filling the missing data with the average rating of the item
        rating_matrix = rating_matrix.fillna(rating_matrix.mean())

        inertias = []

        unique_user_cnt = len(self.ratings_df['userId'].unique())

        # handling exceptional cases where the users are too few
        if unique_user_cnt <= 5:
            return 2

        # choose the number of clusters between 2 to the (total number of unique users - 1) / 2
        # limiting up to 5 clusters as too many clusters make it harder to choose an option among them
        K = range(1, 1+5)

        kmeanModels = []

        for k in K:
            kmeanModel = KMeans(n_clusters=k)
            kmeanModel.fit(rating_matrix)

            # keeping the current model until we know the desirable k
            kmeanModels.append(kmeanModel)

            # Inertia is the sum of the squared distainces of *samples* to their closest cluster center
            inertia = kmeanModel.inertia_
            inertias.append(inertia)

        # we look for the *elbow* here
        # elbow is the number of clusters
        # where the linearly decreasing inertia starts to decrease slower than the previous numbers
        for idx in range(0, len(inertias)):
            # excluding 1 cluster at idx 0 because 1 will make the hierarchical clustering infinite
            if idx == 0:
                pass
            elif inertias[idx - 1] - inertias[idx] > inertias[idx] - inertias[idx + 1]:
                self.cluster_labels = kmeanModels[idx].labels_
                return idx + 1
            # if there's no elbow at last, return the last idx
            elif idx == len(inertias) - 1:
                self.cluster_labels = kmeanModels[idx].labels_
                return idx + 1




