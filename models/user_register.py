from db import db
from models.enums import UserTypes


class AllUsers(db.Model):
    __tablename__ = "registered_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(220), nullable=False)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    role = db.Column(db.Enum(UserTypes), default=UserTypes.user, nullable=True)
    verified = db.Column(db.Boolean, default=False)