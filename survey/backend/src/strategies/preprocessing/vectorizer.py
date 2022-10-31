

class Vectorizer:
    def __init__(self, rating_df):
        self.rating_df = rating_df
        
    def compress_sparse_ids(self):
        user_ids = self.rating_df["userId"].unique().tolist()
        user2user_encoded = {x: i for i, x in enumerate(user_ids)}

        movie_ids = self.rating_df["movieId"].unique().tolist()
        movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}

        self.rating_df["user"] = self.rating_df["userId"].map(user2user_encoded)
        self.rating_df["movie"] = self.rating_df["movieId"].map(movie2movie_encoded)