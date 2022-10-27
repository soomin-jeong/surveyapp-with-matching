import json
import importlib
from sqlalchemy import exc

from survey.backend.src.utils.create_item_descriptions import create_item_descriptions
from survey.backend.src.app import db
from survey.backend.src.database.models.sqlalchemy_classes.dataset import Dataset
from survey.backend.src.database.models.sqlalchemy_classes.survey import Survey
from survey.backend.src.database.models.sqlalchemy_classes.participant import Survey_Participant
from survey.backend.src.database.models.sqlalchemy_classes.response import Response
from survey.backend.src.database.models.sqlalchemy_classes.questionnaire import Questionnaire





######################################################################################
##                              HELPER FUNCTIONS                                    ##
######################################################################################




## helper functions specific to the questionnaire route
## database should be configured (see app.py) and available as db for these to work

## when a post request arrives from the frontend, evaluate it and send
## next item employing the appropriate strategy

"""
    summary: evaluates the incoming request from the frontend to see if the
        request is for the first question or next question
        makes a decision for the first or next item based on current info
        creates description for the said item
        return the complete JSON of the item description
    
    paramters:
        participant_token: unique identifier of the participant, extracted from
        survey URL

        ques_no: current question number, -1 if it's start of the survey

"""

## provide the frontend necessary information about the related survey based
## on the participant token number
def send_survey_details(participant_token):
    rel_questionnaire = db.session.query(Questionnaire).filter_by(token=participant_token).first()
    num_items = rel_questionnaire.num_questions
    survey_name = db.session.query(Survey).filter_by(id=rel_questionnaire.survey_id).first().name
    participant_id = db.session.query(Survey_Participant).filter_by(token=participant_token).first().id
    curr_ratings = None
    prev_session_items = None
    try:
        curr_ratings =json.loads(db.session.query(Response).filter_by(participant_id=participant_id).first().ratings)
        #print(f"already rated items:{type(curr_ratings)}")
        #print(f"already rated items:{(curr_ratings)}")
    except AttributeError as e:
        print("no item rated yet")

    if curr_ratings:
        prev_session_items = [{
            'current_ratings': curr_ratings,
            'next_item': create_item_descriptions(i) 
            }for i in curr_ratings.keys()]
    
    payload_to_send = {
        'survey_name': survey_name,
        'num_items': num_items,
        'ratings': (curr_ratings),
        'previous_session_items': prev_session_items
    }
    return (payload_to_send)




## send description of the next item to be populated on the front end
## along with all current ratings of the user from the db
def send_next_item_and_current_ratings(participant_token):
    rel_participant = db.session.query(Survey_Participant).filter_by(token=participant_token).first()
    ## find out all current ratings given by the same user
    all_curr_ratings = db.session.query(Response).filter_by(participant_id = rel_participant.id).first().ratings


    ## traverse the db to related strategy using the token number
    rel_ques = db.session.query(Questionnaire).filter_by(token=participant_token).first()
    rel_survey = db.session.query(Survey).filter_by(id=rel_ques.survey_id).first()
    rel_dataset = db.session.query(Dataset).filter_by(id=rel_survey.dataset_id).first()
    rel_strategy_name = rel_survey.item_selection_strategy

    ## new item selection strategies are stored in the src/matchmaking folder
    ## each file has a different name but contains a class called Strategy in it

    ## load the related strategy file (module) from the directory
    loaded_module = importlib.import_module(f'.{rel_strategy_name}', 'backend.src.strategies.next_question_selection.implemented_strategies')
    #loaded_module = importlib.import_module(f'.{rel_strategy_name}', '..strategies.item_selection')
    
    
    ## load the Strategy class from the loaded module
    strategy_class_obj = getattr(loaded_module, 'Strategy')

    ## instantiate the loaded class with the dataset path in question
    strategy_class_instance = strategy_class_obj(rel_dataset.file_path)

    if strategy_class_instance:
    ## if the question number shows it's first question asked
        next_item = create_item_descriptions(strategy_class_instance.get_next_item(all_curr_ratings))
        payload ={"current_ratings": json.loads(all_curr_ratings), "next_item": next_item}
        return payload
    
    return {'Error':'Eror in send_next_item_and_current_ratings in /questionnaire'}






"""
    summary: check if the item was already rated by the user
            if so update the appropriate Response object
            otherwise create a new response object and save it to the db
    parameters:
        participant_token: token number used by the participant to identify themselves
                            extracted from the URL the participant uses to log on to the survey
        ratings: rating data present as a JSON with format {itemid:rating}
"""
def save_ratings(particiapant_token, ratings):
    print(f'save ratings:\n current = {ratings.keys()}')
    

    partcipant = db.session.query(Survey_Participant).filter_by(token=particiapant_token).first()
        ## find if a response associated to the user and item exists yet
        ## response should be unique to the participant ID / Token
    resp = db.session.query(Response).filter_by(participant_id = partcipant.id).first()

    
    ## if no response related to the user and item yet create one and save in the db
    if not resp:
        response = Response(ratings=json.dumps(ratings), participant_id=partcipant.id)
        try:
            db.session.add(response)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error {e}")
    ## if the response object already exists, update the rating value only
    else:
        try:
            print("replace old ratings with new ones")
            #curr_ratings = json.loads(resp.ratings)
            resp.ratings = json.dumps(ratings)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error: {e}")
       # print(f"itemid = {itemid}\nrating: {rating}")
    #print(f"itmeid = part_id: {}\nitemid: {itemid}\nrating:{rating}")
    curr_ratings= db.session.query(Response).filter_by(participant_id=partcipant.id).all()
    for r in curr_ratings:
        print(str(r))
## src.strategies.matchmaking



def load_class_dynamically(module_name, relative_path_name, class_name):
    mod =  rel_strategy = importlib.import_module(f'.{module_name}', relative_path_name)
    class_object = getattr(mod, class_name)
    return class_object