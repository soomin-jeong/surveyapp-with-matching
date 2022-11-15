import pandas as pd

from backend.settings import USER_COL_NAME, ITEM_COL_NAME, RATING_COL_NAME


class MatrixBuilder:
    def __init__(self, rating_df: pd.DataFrame):
        self.rating_df = rating_df
        # users may have been dropped from the original input data
        self.original_unique_users = rating_df[USER_COL_NAME].unique()
        self.original_unique_items = rating_df[ITEM_COL_NAME].unique()
        self.original_unique_users_cnt = len(self.original_unique_users)
        self.original_unique_items_cnt = len(self.original_unique_items)

        self.rating_matrix = self._compress_the_ratings_df(self.rating_df)

        # optional data processing: dropping users or items with too few ratings
        # self.drop_users_or_items_with_few_ratings()

    def _drop_users_or_items_with_few_ratings(self):

        # CAVEAT: if # users is less than 1% of # items, it will drop everything
        # In this condition, the application is unlikely to return valid clustering anyways.
        # drop items rated by less than 1% of the users
        self.rating_matrix = self.rating_matrix.dropna(axis='columns', thresh=self.original_unique_users_cnt * 0.1)
        # drop users who rated less than 1% of the items
        self.rating_matrix = self.rating_matrix.dropna(axis='index', thresh=self.original_unique_items_cnt * 0.01)

    def _compress_the_ratings_df(self, rating_df: pd.DataFrame) -> pd.DataFrame:
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
