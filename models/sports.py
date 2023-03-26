from db import db
from models.enums import CoachType, SportType

participant_coach = db.Table('participant_coach',
                             db.Column('participant_id', db.Integer, db.ForeignKey('participants.id')),
                             db.Column('coach_id', db.Integer, db.ForeignKey('coaches.id')))

sport_participant = db.Table('sport_participant',
                             db.Column('participant_id', db.Integer, db.ForeignKey('participants.id')),
                             db.Column('sport_id', db.Integer, db.ForeignKey('sports.id')))


class Sport(db.Model):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True)
    sport_type = db.Column(db.Enum(SportType), nullable=False, unique=True)
    participants = db.relationship('SportParticipants', secondary=sport_participant, backref='sport')
    coaches = db.relationship('SportCoach', backref="sport")


class SportCoach(db.Model):
    __tablename__ = "coaches"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    contact = db.Column(db.String(30), nullable=False)
    type = db.Column(db.Enum(CoachType), default=None, nullable=False)
    participants = db.relationship('SportParticipants', secondary=participant_coach, backref='coach')
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.id'))


class SportParticipants(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
