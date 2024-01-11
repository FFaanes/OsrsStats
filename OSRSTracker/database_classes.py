from flask_sqlalchemy import SQLAlchemy
from run import db


class OSRSPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))