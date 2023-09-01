from ..utils import db
from flask_login import UserMixin

class Poll(db.Model, UserMixin):
    __tablename__ ="polls"
    id = db.Column(db.Integer(), primary_key=True)
    question = db.Column(db.Text(), nullable=False)
    option_one = db.Column(db.String(), nullable=False)
    option_two = db.Column(db.String(), nullable=False)
    option_three = db.Column(db.String(), nullable=False)
    option_one_count = db.Column(db.Integer(), default=0)
    option_two_count = db.Column(db.Integer(), default=0)
    option_three_count = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<User: {self.id}>"
