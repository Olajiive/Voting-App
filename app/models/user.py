from ..utils import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ ="users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text(),  nullable=False)
    datetime = db.Column(db.DateTime(), default=datetime.utcnow)
    poll = db.relationship("Poll", backref="user", lazy=True)

    def __repr__(self):
        return  f"{self.username}"
    
