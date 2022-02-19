"""
This contains the application factory for creating flask application instances.
Using the application factory allows for the creation of flask applications configured
for different environments based on the value of the FLASK_ENV environment variable
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# ## Helper Functions ###
def register_blueprints(app):
    from API_SearchMovies.Search_byID_api.views import api_id

    app.register_blueprint(api_id, url_prefix='')


def register_extensions(app):
    db.init_app(app)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        
        db.session.remove()


# ## Application Factory ###
def create_app(config):

    app = Flask(__name__)

    # Configure the flask app instance
    # CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')

    app.config.from_object(config)
    # app.config.from_object(TaskMgmtSys.config.CONFI)

    # Register blueprints
    register_blueprints(app)

    # Register Extensions
    register_extensions(app)

    # Configure Database
    configure_database(app)

    return app
