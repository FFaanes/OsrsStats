from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# App Configuration
def setup_app():
    # Setup Flask Server
    app = Flask(__name__, template_folder="template")
    app.config["DEBUG"] = False
    app.config["HOST"] = "10.0.0.11"
    app.config["PORT"] = 5000
    app.config["SECRET_KEY"] = "secret_shhh"


    # SQL Alchemy Database setup
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    return app, db



    