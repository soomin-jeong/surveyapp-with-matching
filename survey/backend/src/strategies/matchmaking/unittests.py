import os
import pandas as pd


RATINGS_PATH: str = "../../../data/datasets/movielens_small/ratings.csv"


def test_ratings_file_exist():
    assert os.path.exists(RATINGS_PATH), "The ratings file does not exit. Verify if the path was set properly."


def test_ratings_file_contains_necessary_columns():
    ratings = pd.read_csv(filepath_or_buffer=RATINGS_PATH, sep=',', dtype='str')

    assert list(ratings.columns.values.tolist()) == ['userId', 'movieId', 'rating', 'timestamp'], \
        "The columns are : {}".format(ratings.columns)

def test_naive_strategy_returns_existing_user():
    users_in_ratings =
    matched_user =


