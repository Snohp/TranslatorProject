from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_text = db.Column(db.Text)
    translated_text = db.Column(db.Text)
    create_time = db.Column(
        db.DateTime,
        default=datetime.now
    )