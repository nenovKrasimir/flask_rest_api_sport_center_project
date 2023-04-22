import re

from marshmallow import fields, Schema, validate, validates, validates_schema, ValidationError
from password_strength import PasswordPolicy

from models.user_register import AllUsers


def validate_email(value):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        raise ValidationError('Invalid email address')


class RegisterUserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=25))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=25))
    email = fields.Email(required=True, validate=validate_email)

    @validates('username')
    def duplicate_username(self, username):
        user = AllUsers.query.filter_by(username=username).first()
        if user:
            raise ValidationError("Username is already registered")

    @validates('password')
    def validate_password(self, pw):
        policy = PasswordPolicy.from_names(uppercase=1, numbers=1, special=1, nonletters=1)
        errors = policy.test(pw)
        if errors:
            raise ValidationError(f"Password not strong enough!")

    @validates('email')
    def validate_email(self, value):
        user = AllUsers.query.filter_by(email=value).first()
        if user:
            raise ValidationError('Email already registered!')


class LoginUserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @validates_schema
    def validate_password(self, data, **kwargs):
        user = AllUsers.query.filter_by(username=data['username']).first()
        if not user:
            raise ValidationError('Invalid username or password')


class BuySubscriptionSchema(Schema):
    subscriber_info = fields.Dict(required=True)
    email = fields.Email(required=True, validate=validate_email)
    card_token = fields.String(required=True)
    subscription_id = fields.String(required=True)
    phone = fields.String(required=True)
    region = fields.String(required=True)

    @validates('subscriber_info')
    def validate_info(self, value):
        if not all(k in value for k in ("first_name", "last_name", "identity")):
            raise ValidationError("Invalid subscriber info")

        if len(value["identity"]) != 10:
            raise ValidationError("Identity is with invalid length")


class BuyEquipmentSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True, validate=validate_email)
    type_equipment = fields.String(required=True)
    card_token = fields.String(required=True)
    region = fields.String(required=True)
    contact = fields.String(required=True)

    @validates('type_equipment')
    def validate_equipment(self, value):
        if value not in ["boxing_equipment", "fitness_equipment", "swimming_equipment"]:
            raise ValidationError("Not a valid equipment")
