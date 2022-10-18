import os
import pandas as pd
import json

from collections import Counter
from random import choice
from survey.backend.src.strategies.next_question_selection.rated_by_the_most_strategy import RatedByTheMostStrategy


RATINGS_PATH: str = "../../../data/datasets/movielens_small/ratings.csv"


def test_ratings_file_exist():
    assert os.path.exists(RATINGS_PATH), "The ratings file does not exit. Verify if the path was set properly."


def test_ratings_file_contains_necessary_columns():
    ratings = pd.read_csv(filepath_or_buffer=RATINGS_PATH, sep=',', dtype='str')

    assert list(ratings.columns.values.tolist()) == ['userId', 'movieId', 'rating', 'timestamp'], \
        "The columns are : {}".format(ratings.columns)


def test_rated_by_most_st_has_the_most_ratings():
    ratings = pd.read_csv(filepath_or_buffer=RATINGS_PATH, sep=',', dtype='str')
    rated_by_most_st = RatedByTheMostStrategy(RATINGS_PATH)

    # select a random movie and add it as a movie which is already rated by an online user
    random_movie = choice(ratings['movieId'])
    current_ratings_dict = {random_movie: 5}
    random_from_most_rated_movie_ids = rated_by_most_st.get_next_item(json.dumps(current_ratings_dict))

    # select the movie rated by the most
    most_common_movies = Counter(ratings['movieId'].to_list()).most_common(10)
    most_common_movie_ids = [each[0] for each in most_common_movies]

    assert random_from_most_rated_movie_ids in most_common_movie_ids


