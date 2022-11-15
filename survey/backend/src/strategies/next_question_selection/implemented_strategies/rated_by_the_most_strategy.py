import json
import pandas as pd
import numpy as np
import random
import ast

from backend.src.strategies.next_question_selection.abstract_class.item_selection_base import BaseStrategy
from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from backend.src.strategies.preprocessing.utils import raw_dataset_path

class Strategy(BaseStrategy):
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.clustering = HierarchicalCluster(dataset_name)

    def get_next_item(self, current_ratings: str) -> str:
        
        ##convert the ratings that came as string to dict
        current_ratings_dict = ast.literal_eval(current_ratings)
        already_rated_items = []

        ## for first item, the dict does not contain anything
        if current_ratings_dict:
            already_rated_items = list(ast.literal_eval(current_ratings))

        # value_counts() returns how many times each movie appeared in the ratings in a descending orders
        # index: movie_id, value: count
        most_popular_movies = pd.read_csv(raw_dataset_path(self.dataset_name)).loc[:,'movieId'].value_counts().index.tolist()[:10]
        next_item = random.choice(most_popular_movies)

        # most_popular_movies_minus_already_rated = most_popular_movies.filter(already_rated_items0)
        # next_itme = random.choice(most_popular_movies_minus_already_rated)

        while next_item in already_rated_items:
            next_item = random.choice(most_popular_movies)
        return next_item
    


