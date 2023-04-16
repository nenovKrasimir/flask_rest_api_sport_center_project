from datetime import datetime

from db import db


class OneTimePayments(db.Model):
    __tablename__ = "one_time_payments"

    id = db.Column(db.Integer, primary_key=True)
    paid_by = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
