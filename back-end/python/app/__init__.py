from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_class=None):
    app = Flask(__name__)

    # Load the default configuration base on the environment
    if config_class is None:
        config_class = Config
    app.config.from_object(config_class)
    config_class.init_app(app)

    db.init_app(app)
    CORS(app)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
