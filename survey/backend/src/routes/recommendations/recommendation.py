from flask import Blueprint, request
import json
from flask_cors import cross_origin
import importlib
import pandas as pd


from backend.src.app import db
from backend.src.database.models.sqlalchemy_classes.questionnaire import Questionnaire
from backend.src.database.models.sqlalchemy_classes.survey import Survey
from backend.src.database.models.sqlalchemy_classes.participant import Survey_Participant
from backend.src.database.models.sqlalchemy_classes.response import Response
from backend.src.database.models.sqlalchemy_classes.dataset import Dataset
from .helper_functions import send_recommendations, save_recom_ratings
## createa a blueprint for this route to be easily added to root later.
recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommendation', methods = ['POST', 'GET'])
@cross_origin(supports_credentials=True)
def handle_recommendations():

    if request.method == "GET":
        token = request.args.get("token")
        ## recommendation get is called when a particiapnt has finished answering the survey questions 
        ## i.e. item ratings and now its turn to show him/her the recommendations
        ## an answer to the get request should be all of the recommendation lists to be shown
        ## before sending the recommendatios, matchmaking is to be done using the data gathered from the participant
        
        ## find related dataset based on the token
     
        rel_questionnaire = db.session.query(Questionnaire).filter_by(token=token).first()
        rel_survey = db.session.query(Survey).filter_by(id=rel_questionnaire.survey_id).first()
        rel_dataset = db.session.query(Dataset).filter_by(id=rel_survey.dataset_id).first()
        rel_matchmaking_strategy = rel_survey.matchmaking_strategy
        rel_reclist_files = json.loads(rel_survey.reclist_filenames)
        rel_particiapant = db.session.query(Survey_Participant).filter_by(token=token).first()
        current_ratings = db.session.query(Response).filter_by(participant_id=rel_particiapant.id).first().ratings
          ## new item selection strategies are stored in the src/matchmaking folder
        ## each file has a different name but contains a class called Strategy in it

        ## load the related strategy file (module) from the directory
        loaded_module = importlib.import_module(f'.{rel_matchmaking_strategy}', 'backend.src.strategies.matchmaking.implemented_strategies')
        #loaded_module = importlib.import_module(f'.{rel_strategy_name}', '..strategies.item_selection')
        ## load the Strategy class from the loaded module
        strategy_class_obj = getattr(loaded_module, 'Strategy')
        print(f"recomendations, current ratings = {current_ratings}")

        ## instantiate the loaded class with the dataset path in question
        rating_df = pd.read_csv(filepath_or_buffer=rel_dataset.file_path, sep=',', dtype='str')
        strategy_class_instance = strategy_class_obj(rating_df)

        try:
            matched_offline_user_id = strategy_class_instance.get_matched_offline_user_id(current_ratings)
            return send_recommendations(token, matched_offline_user_id, rel_reclist_files)
        except Exception as e:
            print(f"Unexpected error from send_recommendation in /recommendation")
            raise

    elif request.method == "POST":

        ## recommendation post handles saving the ratings provided by participants for the individual
        ## reocmmendation lists that were shown

        ## token number, reclist num, rating provided by the frontend in POST data.
        data_from_frontend =request.get_json()
        reclist_filenames = data_from_frontend['reclist_filenames']
        offline_user_id = data_from_frontend['offline_user_id']
        ratings = data_from_frontend['ratings']
        token = data_from_frontend['token']

        if save_recom_ratings(token, offline_user_id, json.dumps(reclist_filenames), json.dumps(ratings)) == 0:
            return {'Success': 'Ratings saved successfully'}
        else:
            return {'Error:': 'Ratings could not be saved. Check save save_recom_ratings function in /recommendation route.'}
       
    else:
        return {'Error':'Request could not be handled by both GET and POST in /recommendation route.'}


