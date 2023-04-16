import re

from marshmallow import fields, Schema, validate, validates, validates_schema, ValidationError
from werkzeug.exceptions import BadRequest

from models.enums import CoachType
from models.sports import Coaches


class AddingCoach(Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=25))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=25))
    phone_number = fields.String(required=True)
    coach_type = fields.String(required=True)

    @validates('phone_number')
    def validate_phone_number(self, value):
        if not re.match(r'^(0|\+359)(87|88|89|98|99)[2-9]\d{6}$', value):
            raise ValidationError('Invalid bulgarian phone number')

    @validates('coach_type')
    def validate_type_coach(self, value):
        if value not in CoachType.__members__:
            raise BadRequest("Invalid type of coach")

    @validates_schema
    def validate_name_and_id(self, data, **kwargs):
        coach = Coaches.query.filter_by(first_name=data['first_name']).first()
        try:
            if coach.contact == data['phone_number']:
                raise BadRequest("The coach is already added for this sport")
        except AttributeError:
            return True


class DeletingCoach(Schema):
    id = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)

    @validates_schema
    def validate_name_and_id(self, data, **kwargs):
        coach = Coaches.query.filter_by(id=data['id']).first()
        if not coach:
            raise BadRequest("Their is no coach with that id")
        if coach.participants:
            raise BadRequest("The coach has active participants, cannot be delete it")
        if coach.first_name != data["first_name"]:
            raise BadRequest("First name does not match the ID")
        if coach.last_name != data["last_name"]:
            raise BadRequest("Last name does not match the ID")


class UpdateContactCoach(Schema):
    new_phone_number = fields.String(required=True)
    id = fields.String(required=True)

    @validates('new_phone_number')
    def validate_phone_number(self, value):
        if not re.match(r'^(0|\+359)(87|88|89|98|99)[2-9]\d{6}$', value):
            raise ValidationError('Invalid bulgarian phone number')
