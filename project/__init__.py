import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    """
    Creates a flask app instance and initializes the db. If test_config
    is passed, then app instance for Testing env is created. Else, app
    instance for current Environment is created.
    :param test_config: str
    :return: return flask app instance
    """
    app = Flask(__name__)
    if test_config is None:
        app_settings = os.getenv('APP_SETTINGS')
        app.config.from_object(app_settings)
    else:
        app.config.from_object(test_config)
    db.init_app(app)
    return app

