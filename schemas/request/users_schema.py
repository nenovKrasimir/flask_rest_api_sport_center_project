import re

from marshmallow import fields, Schema, validate, validates, validates_schema, ValidationError
from password_strength import PasswordPolicy

from models.user_register import AllUsers


class RegisterUserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=25))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=25))
    email = fields.Email(required=True)

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
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValidationError('Invalid email address')


class LoginUserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @validates_schema
    def validate_password(self, data, **kwargs):
        user = AllUsers.query.filter_by(username=data['username']).first()
        if not user:
            raise ValidationError('Invalid username or password')
