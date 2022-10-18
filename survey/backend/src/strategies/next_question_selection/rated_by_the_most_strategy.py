import json
import pandas as pd
import numpy as np
import random
from .abstract_class.item_selection_base import BaseStrategy
import ast


class RatedByTheMostStrategy(BaseStrategy):
    def __init__(self, dataset_path: str):
        self.__dataset_path= dataset_path
            
       # self.__50_most_pop_movies = dict()
            
    @property
    def dataset_path(self: str):
        return self.__database_path
    
    @dataset_path.setter
    def dataset_path(self, value: str):
        self.__dataset_path = value

    def get_next_item(self, current_ratings: str) -> str:
        
        ##convert the ratings that came as string to dict
        current_ratings_dict = ast.literal_eval(current_ratings)
        already_rated_items = []

        ## for first item, the dict does not contain anything
        if current_ratings_dict:
            already_rated_items = list(ast.literal_eval(current_ratings))

        try:
            dataset = pd.read_csv(filepath_or_buffer= self.__dataset_path, sep=',', dtype='str')
          
        except FileNotFoundError as e:
            print("ERROR:\nmost_popular_selection:file not found")
            return e

        # value_counts() returns how many times each movie appeared in the ratings in a descending orders
        # index: movie_id, value: count
        most_popular_movies = dataset.loc[:,'movieId'].value_counts().index.tolist()[:10]
        next_item = random.choice(most_popular_movies)

        # most_popular_movies_minus_already_rated = most_popular_movies.filter(already_rated_items0)
        # next_itme = random.choice(most_popular_movies_minus_already_rated)

        while next_item in already_rated_items:
            next_item = random.choice(most_popular_movies)
        return next_item
    


