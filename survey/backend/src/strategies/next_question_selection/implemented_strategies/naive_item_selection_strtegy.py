import json
import pandas as pd
import numpy as np
import random
from survey.backend.src.strategies.next_question_selection.abstract_class.item_selection_base import BaseStrategy
import ast
## instantiations of base strategy
## add new classes here for custom item selection strategies
class Strategy(BaseStrategy):
    def __init__(self, dataset_path):
        self.__dataset_path= dataset_path
            
    @property
    def dataset_path(self):
        return self.__database_path
    
    @dataset_path.setter
    def dataset_path(self, value):
        self.__dataset_path = value

    
    def get_next_item(self, current_ratings):
        current_ratings_dict = ast.literal_eval(current_ratings)
        last_item=1
        if list(current_ratings_dict.keys()):
            last_item = list(ast.literal_eval(current_ratings).keys())[-1]
        print(f"get_next_item: current rated items {last_item}")
        dataset = ""
        try:
            dataset = pd.read_csv(filepath_or_buffer= self.__dataset_path, sep=',', dtype='str')
          
        except FileNotFoundError as e:
            print("ERROR:\nnaive_item_selection:file not found")
            return e

        ## select a random item
        item = dataset.sample(axis="rows")
        all_unique_itemIds = (dataset['movieId'].unique().tolist())[0:50]

        next_item = random.choice(all_unique_itemIds)

        ## send the movie id only
        rand_movie_id_int = int(item['movieId'].values[0])
        return next_item


