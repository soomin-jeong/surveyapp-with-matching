from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_mail import Mail

#from survey.backend.src.database.models.survey import Survey
#from .utils.utils import generate_random_tokens

from .flask_configs import Flask_Configs


db = SQLAlchemy()
mail = Mail()
def create_app():

    app= Flask(__name__)

    

    ### Load app configurations from another file

    app.config.from_object(Flask_Configs)
    mail.init_app(app)

   ## import all models before initializing the database
    from .database.models.sqlalchemy_classes.survey import Survey
    from .database.models.sqlalchemy_classes.dataset import Dataset
    from .database.models.sqlalchemy_classes.offline_eval import Offline_eval
    from .database.models.sqlalchemy_classes.participant import Survey_Participant
    from .database.models.sqlalchemy_classes.question import Question
    from .database.models.sqlalchemy_classes.questionnaire import Questionnaire
    from .database.models.sqlalchemy_classes.reclist import RecommendationList_Model
    from .database.models.sqlalchemy_classes.reclist_questionnaire import Reclist_Questionnaire
    from .database.models.sqlalchemy_classes.reclist_question import Reclist_Question
    from .database.models.sqlalchemy_classes.reclist_response import Reclist_Response
    from .database.models.sqlalchemy_classes.response import Response
    #from .database.models.sqlalchemy_classes.algorithm import Algorithm
    
    ##initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    ##configure cors so that the react frontend can communicate with it.
  #  from database.models import Survey_Model, Questionnaire_Model

    ## import the blueprints for individual routes from routes directory
    from .routes.questionnaire.questionnaire import questionnaire_bp
    #from .routes.offline_eval import offline_eval_bp
    from .routes.recommendations.recommendation import recommendation_bp
    from .routes.survey.survey import survey_bp

    ## register blueprints so that they can be accessed as routes to the webapps
    app.register_blueprint(questionnaire_bp)
    app.register_blueprint(survey_bp)
    #app.register_blueprint(offline_eval_bp)
    app.register_blueprint(recommendation_bp)

    ## create the actual tables in the db
  
    cors = CORS(app, supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'

    return app


app = create_app()




## running the app on localhost and default port 5000.
if '__name__' == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)