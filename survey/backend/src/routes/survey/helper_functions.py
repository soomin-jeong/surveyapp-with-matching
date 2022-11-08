from dataclasses import dataclass
from sqlite3 import DatabaseError
import json
import csv
from flask_mail import Message
from smtplib import SMTPException
from sqlalchemy import exc


from ...app import db, mail
from ...utils.utils import generate_random_tokens, list_directory_files, list_subdirectoreis
from ...utils.create_item_descriptions import create_item_descriptions
from ...database.models.sqlalchemy_classes.dataset import Dataset
from ...database.models.sqlalchemy_classes.question import Question
from ...database.models.sqlalchemy_classes.questionnaire import Questionnaire
from ...database.models.sqlalchemy_classes.survey import Survey
from ...database.models.sqlalchemy_classes.participant import Survey_Participant
from ...utils.logger import api_logger








######################################################################################
##                                  HELPER FUNCTIONS                                ##
######################################################################################


''''
Collect the information about the surveys, datasets, offline evaluations, strategies, and more
to the frontend.

'''
def collect_frontend_dashboard_data():
    all_data = {
                'surveys': [],
                'datasets': [],
                'offline_evals': [],
                'reclists': [],
                'strategies':{
                    'matchmaking':[],
                    'item_selection':[]
                   
                },
                 'mailing_lists':[]
                }
    ## list all surveys
    all_surveys = db.session.query(Survey).all()
    if all_surveys:
        for s in all_surveys:
            ## add json formatted string representation of those surveys to the list
            all_data['surveys'].append(str(s))


    all_datasets_in_db = db.session.query(Dataset).all()
    dataset_dirs = list_subdirectoreis(('backend/data/datasets'))
    #dataset_dirs = list_subdirectoreis(os.path.abspath('../data/datasets'))
    if dataset_dirs:
        for d in dataset_dirs:
            create_new_dataset(d, f'{("backend/data/datasets")}/{d}/ratings.csv')
    if all_datasets_in_db:
        for  d1 in all_datasets_in_db:
            if d1.name not in dataset_dirs:
                try:
                    db.session.delete(d1)
                    db.session.commit()
                    print(f"deleted database {d1.name}")
                except exc.SQLAlchemyError as e:
                    db.session.rollback()
                    print(e)

    all_datasets = db.session.query(Dataset).all()

    ## get name of all reclist files from the directory
    #all_reclists = list_directory_files(os.path.abspath('../data/recommendation_lists'))
    all_reclists = list_directory_files(('backend/data/recommendation_lists'))
    for l in all_reclists:
        all_data['reclists'].append(l)
    
    all_mailing_lists = list_directory_files(('backend/data/mailing_lists'))
    for l in all_mailing_lists:
        all_data['mailing_lists'].append(l)
    ## ifo about all datasets
    if all_datasets:
        for d in all_datasets:
            all_data['datasets'].append(str(d))
    #all_matchmaking_strategies = list_directory_files('strategies/matchmaking')
    #all_item_selection_strategies = list_directory_files('strategies/item_selection')
    all_matchmaking_strategies = list_directory_files('backend/src/strategies/matchmaking')
    all_item_selection_strategies = list_directory_files('backend/src/strategies/next_question_selection')
    for s in all_matchmaking_strategies:
        all_data['strategies']['matchmaking'].append(s)
    for s in all_item_selection_strategies:
        all_data['strategies']['item_selection'].append(s)
    return json.dumps(all_data)








'''
    Take the file path of a dataset and add it to the database.
    NOTE: the actual database object is not saved, just the path is saved in the DB
    dataset.load_dataset() loads the said dataset from the file path as a pandas dataframe

'''
def create_new_dataset(name, file_path):
    ds_in_db = db.session.query(Dataset).filter_by(name=name).first()
    if ds_in_db:
        print(f"Dataset with the name already exists")
    else:
        ds = Dataset(name=name, file_path=file_path)
        try:
            db.session.add(ds)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(e)








'''
Create database objects initializing a survey
Also create specified number of survey questionnaire and participant objects
Create specified number of random strings to act as unique tokens and assign these
to the questionnaire and participant objects.
    def __str__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'num_items': self.num_items,
            'num_questions': self.num_tokens,
            'description': self.description,
            'tokens': self.tokens,
            'dataset_id': self.dataset_id,
            'matchmaking_strategy': self.matchmaking_strategy,
            'item_selection_strategy': self.item_selection_strategy,
            'reclist_filenames': self.reclist_filenames,
            'active_status':self.active_status
        })
'''
def create_new_survey(name, 
                    description,
                    dataset_name, 
                    num_participants, 
                    num_questions, 
                    item_selection_strategy, 
                    matchmaking_strategy,
                    mailing_list,
                    reclists_for_online_eval,
                    active_status = "created"):
 

    ## find out the related dataset
    res_dataset = db.session.query(Dataset).filter_by(name=dataset_name).first()

    ## TODO: if the preprocessing and hierachical clustering was already run, load the preprocessed class

    ## TODO: else, run the preprocessing and hierarchical clustering and save the results

    ## random tokens
    #tokens = [generate_random_tokens(16) for n in range(0,num_participants)]
    ## print(str(tokens))
    
    ## create survey with its database being the one created above
    test_survey1 = Survey(name=name, 
    num_tokens=num_participants,
    num_questions=num_questions,
    dataset_id=res_dataset.id,
    description=description, 
    matchmaking_strategy=matchmaking_strategy, 
    item_selection_strategy=item_selection_strategy, 
    #tokens=json.dumps(tokens), 
    reclist_filenames=json.dumps(reclists_for_online_eval),
    mailing_list = mailing_list,
    active_status = active_status)
    try:
        db.session.add(test_survey1)
        db.session.commit()
        api_logger.info(f"Survey with name {name} created successfully.")
    except exc.IntegrityError as e:
        db.session.rollback()
        api_logger.error(f"Survey with {name} could not be created. SQLAlchemy error.")
    
    ## find the survey created just now on the DB
    result_test = db.session.query(Survey).filter_by(name=name).first()

    ## create a questionnaire for every token
    


    created_survey = db.session.query(Survey).filter_by(name=name).first()
    return(str(created_survey))

'''
    change the status of a survey to denote not started yet, started and finished
    action = created, started, finished
'''
def start_stop_survey(survey_id, action):
    survey = db.session.query(Survey).filter_by(id=survey_id).first()
    survey_state = None
    survey_num_participants = 0
    mailing_list_filepath = f'backend/data/mailing_lists/{survey.mailing_list}.csv'
    if(action == "start"):
        print("starting")
        all_emails = []
        with open(mailing_list_filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            for r in reader:
                all_emails = all_emails + r
        ## remove spaces in front and at back of the individual emails
        all_emails = [email.strip() for email in all_emails]


        ## filter out all emails that are not in correct format, i.e. abc@def.ghi
        all_emails = list(filter(lambda e: ('@' in e and '.' in e), all_emails))
        tokens = [generate_random_tokens(16) for n in range(0,len(all_emails))]
        survey_num_participants = len(all_emails)
        for t in tokens:
            ques1 = Questionnaire(survey_id=survey.id, token=t, num_questions=survey.num_questions)
            try:
                db.session.add(ques1)
                db.session.commit()
            except:
                db.session.rollback()
                print(f"Error: {e}")
        
    ## create a participant for each token
        for t in tokens:
            participant = Survey_Participant(survey_id= survey.id, token=t,)
            try:
                db.session.add(participant)
                db.session.commit()
            except:
                db.session.rollback()
                print(f"Error: {e}")
        print("whatwhat")
        try:
            survey.tokens=json.dumps(tokens)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            print("could not add token to the survey")
            db.session.rollback()
        
        print(f"sending emails to all tokens")
        for e, tok in zip(all_emails, tokens):
            print(f"seding email to {e}.")
            send_email_to_user(e, mail, tok)
        print(all_emails)
        survey_state = "started"
    elif(action == "finish"):
        survey_state = "finished"
    elif(action == "create"):
        survey_state = "created"
    else:
        api_logger.error(f"State Error. Could not change the state of the survey to {action}.")
      
    try:
        survey.num_participants = survey_num_participants
        survey.active_status = survey_state
        db.session.commit()
    except:
        db.session.rollback()
        api_logger.error(f" Database Error: Could not change the state of the survey to {action}.")




def send_email_to_user(email, mail_client, token):
        #ile = f'backend/data/mailing_lists/{mailing_list_filename}.csv'
        url = f'http://localhost:3000/survey?token={token}'
        msg = Message("Invitation to take part the Recommender System Survey.",
                        sender="therh1992@gmail.com", recipients=[email])
        print(url)
        msg.body = 'Please follow the following the following link: ' + url
        msg.html = f'<b>Hello</b>, <p>Please follow this <a href="{url}">invitation link</a>, to participate in the survey.</p>' 
        try:
            mail_client.send(msg)
            api_logger.info(f"Successfully sent email to {email}")
          
        except SMTPException as e:
            api_logger.error(f"Could not send email to {email}\nTry manually using this URL: {url}")

           