import os
import pandas as pd
import omdb

##iniitialize omdb api
## TODO: move sensitive information (api key) to a separate file
omdb_client = omdb.OMDBClient(apikey="afb2e202") # 85798af afb2e202 aa5a8680

'''
Create a description about each item to show on the frontend.
It can have any structure you like, but must be picked up correctly by
the frontend to display items.


'''
def create_item_descriptions(item_id):
    
    """ Provide description (id, description) for survey questionnaire items
        Change this function to suit your to create item descriptions
        frontend should be adapted to cater to the changes made here

    Args:
        item_id ([int]): ids of the items (from dataset)
    """
    try:
        movies_file_abspath = os.path.abspath("survey/backend/data/datasets/movielens_small/movies.csv")
        #movies_file_abspath = os.path.abspath('../data/datasets/movielens_small/movies.csv')
        item_labels_df = pd.read_csv(movies_file_abspath, dtype='str')
        #print(item_labels_df)
        
        links_file_abspath = os.path.abspath("survey/backend/data/datasets/movielens_small/links.csv")
        #links_file_abspath = os.path.abspath("../data/datasets/movielens_small/links.csv")
        imdb_id_links = pd.read_csv(links_file_abspath,dtype='str')
        ## build imdb ids from the imdb <-> omdb <-> movieId relationships extracted from links.csv
    
        imdb_id_int = imdb_id_links.loc[imdb_id_links['movieId'] == str(item_id)]['imdbId'].values[0]
        imdb_id = 'tt'+imdb_id_int


        ## send request to to the omdb api for detailled information for the given imdb id
        omdb_ans = omdb_client.imdbid(imdb_id)#, tomatoes=False)
        description = {
            'item_id': item_id,
            'description':{
                'movie_id': item_id,
                'imdb_id': imdb_id,
                'title': omdb_ans['title'],
                'year':omdb_ans['year'],
                'genre': omdb_ans['genre'],
                'director': omdb_ans['director'],
                'writer': omdb_ans['writer'],
                'actors': omdb_ans['actors'],
                'plot': omdb_ans['plot'],
                'poster': omdb_ans['poster']
            }


        }

        return description
    except FileNotFoundError as e:
        return f'ERROR: module: utils.create_item_descriptions, error:{e}'
