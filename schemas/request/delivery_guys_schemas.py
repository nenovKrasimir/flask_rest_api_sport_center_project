import re

from marshmallow import fields, Schema, validates, validates_schema, ValidationError
from werkzeug.exceptions import BadRequest

from models.delivery_guys import DeliveryGuys


class AddingDeliveryGuy(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    region = fields.String(required=True)
    contact = fields.String(required=True)

    @validates('contact')
    def validate_phone_number(self, value):
        if not re.match(r'^(0|\+359)(87|88|89|98|99)[2-9]\d{6}$', value):
            raise ValidationError('Invalid bulgarian phone number')

    @validates('region')
    def validate_region(self, value):
        if value not in ["Sofia", "Varna", "Burgas"]:
            raise ValidationError('Invalid region for delivery')


class DeletingDeliveryGuy(Schema):
    id = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)

    @validates_schema
    def validate_name_and_id(self, data, **kwargs):
        delivery_guy = DeliveryGuys.query.filter_by(id=data['id']).first()
        if not delivery_guy:
            raise BadRequest("Their is no delivery guy with that id")
        if delivery_guy.packages:
            raise BadRequest("The delivery guy has active packages, cannot be delete it")
        if delivery_guy.first_name != data["first_name"]:
            raise BadRequest("First name does not match the ID")
        if delivery_guy.last_name != data["last_name"]:
            raise BadRequest("Last name does not match the ID")


class UpdateContactDeliveryGuy(Schema):
    id = fields.String(required=True)
    new_contact = fields.String(required=True)

    @validates('new_contact')
    def validate_phone_number(self, value):
        if not re.match(r'^(0|\+359)(87|88|89|98|99)[2-9]\d{6}$', value):
            raise ValidationError('Invalid bulgarian phone number')

    @validates('id')
    def validate_id(self, value):
        print(value)
        if int(value) not in (x.id for x in DeliveryGuys.query):
            raise BadRequest("No coach with that id")


class DeliveryPackages(Schema):
    recipient_name = fields.String(required=True)
    recipient_region = fields.String(required=True)
    recipient_contact = fields.String(required=True)
    status = fields.String(required=True)
    expected_delivery_date = fields.String(required=True)
    delivered_by = fields.String(required=True)

    @validates('recipient_contact')
    def validate_phone_number(self, value):
        if not re.match(r'^(0|\+359)(87|88|89|98|99)[2-9]\d{6}$', value):
            raise ValidationError('Invalid bulgarian phone number')

    @validates("recipient_region")
    def validate_region(self, value):
        if value not in ["Sofia", "Varna", "Burgas"]:
            raise ValidationError('Invalid region for delivery')

