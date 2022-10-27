import json
import pandas as pd
import numpy as np
from survey.backend.src.strategies.next_question_selection.abstract_class.item_selection_base import BaseStrategy
import ast


class Strategy(BaseStrategy):
    def __init__(self, rating_df: pd.DataFrame):
        self.rating_df = rating_df

    def get_next_item(self, current_ratings):
        current_ratings_dict = ast.literal_eval(current_ratings)
        last_item=42
        if list(current_ratings_dict.keys()):
            last_item = list(ast.literal_eval(current_ratings).keys())[-1]
        print(f"get_next_item: current rated items {last_item}")

        ## select a random item
        item = self.rating_df.sample(axis="rows")
        all_unique_itemIds = (self.rating_df['movieId'].unique().tolist())
        ind = all_unique_itemIds.index(str(last_item))
        print(f'index {ind}')
        next_item = all_unique_itemIds[ind+1]
      

        id = (all_unique_itemIds[ind +1])

        ## send the movie id only
        rand_movie_id_int = int(item['movieId'].values[0])
        return id


