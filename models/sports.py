import warnings
from datetime import datetime

from db import db
from models.enums import CoachType, SportType

warnings.filterwarnings('ignore', '.*relationship .* will copy column .*')

participant_coach = db.Table('participant_coach',
                             db.Column('participant_id', db.Integer, db.ForeignKey('participants.id')),
                             db.Column('coach_id', db.Integer, db.ForeignKey('coaches.id')))

sport_participant = db.Table('sport_participant',
                             db.Column('participant_id', db.Integer, db.ForeignKey('participants.id')),
                             db.Column('sport_id', db.Integer, db.ForeignKey('sports.id')))

participant_subscriptions = db.Table('participant_subscription',
                                     db.Column('participant_id', db.Integer, db.ForeignKey('participants.id')),
                                     db.Column('subscription_id', db.Integer, db.ForeignKey('active_subscriptions.id')))


class Sports(db.Model):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True)
    model_type = db.Column(db.Enum(SportType), nullable=False)
    coaches = db.relationship('Coaches', backref="sport")
    participants = db.relationship('Participants', secondary=sport_participant)


class Coaches(db.Model):
    __tablename__ = "coaches"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    contact = db.Column(db.String(30), nullable=False)
    model_type = db.Column(db.Enum(CoachType), default=None, nullable=False)
    participants = db.relationship('Participants', secondary=participant_coach)
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.id'))


class Participants(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    identity = db.Column(db.String(150), nullable=False)
    sports = db.relationship('Sports', secondary=sport_participant)
    coach = db.relationship('Coaches', secondary=participant_coach)
    subscriptions = db.relationship("ActiveSubscription", secondary=participant_subscriptions)


class ActiveSubscription(db.Model):
    __tablename__ = "active_subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    expiration_date = db.Column(db.DateTime, default=datetime.utcnow)
    participants = db.relationship('Participants', secondary=participant_subscriptions)
