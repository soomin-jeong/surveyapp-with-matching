import os
import pandas as pd
import json
import numpy as np

from collections import Counter
from random import choice
from survey.backend.src.strategies.next_question_selection.rated_by_the_most_strategy import RatedByTheMostStrategy

DUMMY_RATINGS = pd.DataFrame(data=np.array([['459', '5618', '5.0', '1520233615'],
                                            ['477', '5618', '4.0', '1201159360'],
                                            ['298', '5618', '2.5', '1447598312'],
                                            ['219', '1262', '3.5', '1194685902'],
                                            ['483', '1262', '3.5', '1178293076'],
                                            ['45', '1262', '5.0', '1020802351'],
                                            ['606', '1262', '3.5', '1184619962'],
                                            ['290', '1084', '5.0', '974938169'],
                                            ['445', '6016', '2.0', '1454621781'],
                                            ['455', '440', '3.0', '836436201']]),
                             columns=['userId', 'movieId', 'rating', 'timestamp'])


def test_rated_by_most_st_has_the_most_ratings():
    rated_by_most_st = RatedByTheMostStrategy(DUMMY_RATINGS)

    # select a random movie and add it as a movie which is already rated by an online user
    random_movie = choice(DUMMY_RATINGS['movieId'])
    current_ratings_dict = {random_movie: 5}
    random_from_most_rated_movie_ids = rated_by_most_st.get_next_item(json.dumps(current_ratings_dict))

    # select the movie rated by the most
    most_common_movies = Counter(DUMMY_RATINGS['movieId'].to_list()).most_common(10)

    # column at index 0: movie IDs
    most_common_movie_ids = [each[0] for each in most_common_movies]

    assert random_from_most_rated_movie_ids in most_common_movie_ids


