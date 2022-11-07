import pandas as pd
import numpy as np


# TODO: move these arbitrary names into the settings file
#  so that users can specify the names when entering the input data file
USER_COL_NAME = 'userId'
ITEM_COL_NAME = 'movieId'
RATING_COL_NAME = 'rating'


class MatrixBuilder:
    def __init__(self, rating_df: pd.DataFrame):
        self.rating_df = rating_df
        # users may have been dropped from the original input data
        self.original_unique_users = rating_df[USER_COL_NAME].unique()
        self.original_unique_items = rating_df[ITEM_COL_NAME].unique()
        self.original_unique_users_cnt = len(self.original_unique_users)
        self.original_unique_items_cnt = len(self.original_unique_items)

        self.drop_users_with_too_sparse_data()

        self.rating_matrix = self.merge_and_transpose_ratings(self.rating_df)

    def drop_users_with_too_sparse_data(self):
        # drop users who rated less than 1% of the items
        if self.original_unique_users_cnt > 30:
            rating_cnt = self.rating_df.groupby([USER_COL_NAME])[ITEM_COL_NAME].count()
            users_rated_certain_num_of_items = rating_cnt[rating_cnt > self.original_unique_items_cnt * 0.01].index.tolist()
            self.rating_df = self.rating_df[self.rating_df[USER_COL_NAME].isin(users_rated_certain_num_of_items)]

        # drop items which were rated by less than 1% of the users
        if self.original_unique_items_cnt > 30:
            rating_cnt = self.rating_df.groupby([ITEM_COL_NAME])[USER_COL_NAME].count()
            items_rated_by_certain_num_of_users = rating_cnt[rating_cnt > self.original_unique_users_cnt * 0.01].index.tolist()
            self.rating_df = self.rating_df[self.rating_df[ITEM_COL_NAME].isin(items_rated_by_certain_num_of_users)]


    def merge_and_transpose_ratings(self, rating_df: pd.DataFrame) -> pd.DataFrame:
        self.original_unique_users.sort()
        self.original_unique_items.sort()

        # generate empty rating dataframe [# users * # items]
        rating_matrix = pd.DataFrame([[None] * len(self.original_unique_items)] * len(self.original_unique_users))

        # rename the index and columns (index=user_id, col=item_id)
        idx_name_mapper = {}
        col_name_mapper = {}

        for idx, user_id in enumerate(self.original_unique_users):
            idx_name_mapper.update({idx: user_id})

        for idx, item_id in enumerate(self.original_unique_items):
            col_name_mapper.update({idx: item_id})

        rating_matrix = rating_matrix.rename(index=idx_name_mapper, columns=col_name_mapper)

        # go through every row in ratings and update the ratings matrix
        for idx, row in rating_df.iterrows():
            rating_matrix.loc[row[USER_COL_NAME], row[ITEM_COL_NAME]] = row[RATING_COL_NAME]

        return rating_matrix
