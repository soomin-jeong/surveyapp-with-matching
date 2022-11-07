import pandas as pd
import numpy as np


class MatrixBuilder:
    def __init__(self, rating_df: pd.DataFrame):
        self.rating_df = rating_df
        self.rating_matrix = self.merge_and_transpose_ratings(self.rating_df)

    '''
    This func reformats the ratings dataframe. 
    Input: a pd.DataFrame whose columns are [userId, movieId, rating, timestamp]
    Output: a pd.DataFrame whose columns are [userId, (all the movie Ids as columns)... rating]

    This step is necessary for the k-means clustering as it requires all the ratings of one user in one row.    
    '''
    def merge_and_transpose_ratings(self, rating_df: pd.DataFrame) -> pd.DataFrame:
        unique_users = rating_df['userId'].unique()
        unique_users.sort()
        unique_items = rating_df['movieId'].unique()
        unique_items.sort()

        # generate empty rating dataframe [# users * # items]
        rating_matrix = pd.DataFrame([[None] * len(unique_items)] * len(unique_users))

        # rename the index and columns (index=user_id, col=item_id)
        idx_name_mapper = {}
        col_name_mapper = {}

        for idx, user_id in enumerate(unique_users):
            idx_name_mapper.update({idx: user_id})

        for idx, item_id in enumerate(unique_items):
            col_name_mapper.update({idx: item_id})

        rating_matrix = rating_matrix.rename(index=idx_name_mapper, columns=col_name_mapper)

        # go through every row in ratings and update the ratings matrix
        for idx, row in rating_df.iterrows():
            rating_matrix.loc[row['userId'], row['movieId']] = row['rating']

        return rating_matrix
