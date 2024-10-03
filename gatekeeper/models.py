from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class GateStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=True)  # True = open, False = closed
    last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
