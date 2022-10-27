import json
import pandas as pd
import numpy as np
import random
from .abstract_class.item_selection_base import BaseStrategy
import ast


class Strategy(BaseStrategy):
    def __init__(self, rating_df: pd.DataFrame):
        self.rating_df = rating_df

    def get_next_item(self, current_ratings: str):
        current_ratings_dict = ast.literal_eval(current_ratings)
        last_item = 1
        if list(current_ratings_dict.keys()):
            last_item = list(ast.literal_eval(current_ratings).keys())[-1]
        print(f"get_next_item: current rated items {last_item}")

        ## select a random item
        all_unique_itemIds = (self.rating_df['movieId'].unique().tolist())[:50]

        next_item = random.choice(all_unique_itemIds)
        return next_item


