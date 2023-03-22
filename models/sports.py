from db import db
from models.enums import UserTypes


class CoachParticipant(db.Model):
    __tablename__ = 'coach_participant'
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'), primary_key=True)


class SportParticipant(db.Model):
    __tablename__ = 'sport_participant'
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.id'), primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'), primary_key=True)


class Sport(db.Model):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True)
    sport_name = db.Column(db.String, nullable=False, unique=True)
    coaches = db.relationship('SportCoach', backref='sport')
    participants = db.relationship('SportParticipant', secondary='sport_participant')


class SportCoach(db.Model):
    __tablename__ = "coaches"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    contact = db.Column(db.String(120), nullable=False, unique=True)
    role = db.Column(db.Enum(UserTypes), default=UserTypes.trainer, nullable=True)
    participants = db.relationship('SportParticipant', secondary='coach_participant')


class SportParticipants(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    coaches = db.relationship('SportCoach', secondary='coach_participant')
    sports = db.relationship('Sport', secondary='sport_participant')
