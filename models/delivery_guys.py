from db import db


class DeliveryGuys(db.Model):
    __tablename__ = "delivery_guys"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=False)
    packages = db.relationship('DeliveryPackages', backref='delivery_guy', lazy=True)


class DeliveryPackages(db.Model):
    __tablename__ = "delivery_packages"

    id = db.Column(db.Integer, primary_key=True)
    recipient_name = db.Column(db.String, nullable=False)
    recipient_region = db.Column(db.String, nullable=False)
    recipient_contact = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="Undelivered", nullable=True)
    expected_delivery_date = db.Column(db.Date, nullable=False)
    delivered_by = db.Column(db.Integer, db.ForeignKey('delivery_guys.id'), nullable=False)
