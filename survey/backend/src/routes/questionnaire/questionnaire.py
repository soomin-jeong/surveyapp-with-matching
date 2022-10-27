
from flask import Blueprint, request
import json

from flask_cors import cross_origin
from .helper_functions import save_ratings, send_next_item_and_current_ratings, send_survey_details

## create a blueprint for this route to be easily added to root later.
questionnaire_bp = Blueprint('questionnaire', __name__)




@questionnaire_bp.route('/questionnaire', methods = ['POST', 'GET'])
@cross_origin(supports_credentials=True)
def handle_questionnaire():

    if request.method == "GET":
        token = request.args.get('token')
        print(f"token = {token}")
        survey_info = send_survey_details(token)
        return json.dumps(survey_info)
    
    elif request.method == "POST":

        ## this route handles the ratings provided by the survey participant for each item
        ## format of data from frontend
        ''' {
            'token': 'jdasfhkjh',
            'ratings': '{234: 5.0, 5739:3.5,..}'
            }
        '''
        ## get data from the body of the post request.
        post_json_data = json.loads(request.get_json()) ## questionnaire_response
        tok = (post_json_data)['token']
        ratings = post_json_data['ratings']

        #print(f"ratings from frontend : {ratings}")
        
        ## call helper function to save the rating provided by the frontend to the db
        save_ratings(tok, ratings)

        ## call helper function to provide (first) or next item
        next_item_and_ratings = send_next_item_and_current_ratings(tok)

        '''
            format of data sent to the frontend
            {
                current_ratings: {'126:'3.0', 48675: '1.0', '539':4.0 ..},
                'next_item': {
                    'item_id': 1625,
                    'description': {
                        'movie_id': 1625, 
                        'imdb_id': 'tt0119174', 
                        'title': 'The Game', 
                        'year': '1997', 
                        'genre': 'Drama, Mystery, Thriller', 
                        'director': 'David Fincher', 
                        'writer': 'John Brancato, Michael Ferris', 
                        'actors': 'Michael Douglas, Deborah Kara Unger, Sean Penn', 
                        'plot': 'After a wealthy San Francisco....', 
                        'poster': 'https://<poster URL>'}}

                }
            }
        '''
        #print(next_item_and_ratings)

        ## return the item description to the frontend
        return next_item_and_ratings
    else:
        ## on rare occassions when the request does not correspond to eithre get or post
        return "Error: Illegal request."








