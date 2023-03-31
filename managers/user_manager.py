import os

from dotenv import load_dotenv
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth_manager import TokenManger
from models.user_register import AllUsers
from services.simple_email_service_aws import EmailService

dir_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(dir_path, '.env'))

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_REGION")
server_adress = os.getenv("SERVER_ADRESS")


class RegisterUser:
    @staticmethod
    def register_user(data):
        data['password'] = generate_password_hash(data['password'])
        user = AllUsers(**data)
        db.session.add(user)
        db.session.commit()
        email_token = TokenManger.encode_email_verify_token(user)
        email_service = EmailService(access_key, secret_key, server_adress, region_name)
        email_service.send_registration_confirmation_email(data["email"], email_token)

    @staticmethod
    def verify_user(token):
        user_data = TokenManger.decode_email_verify_token(token)
        user = AllUsers.query.filter_by(email=user_data['email']).first()
        if not user:
            raise BadRequest("Not a valid page")

        if not user.verified:
            user.verified = True
            db.session.commit()
            return {"Success": "Your account is verified you can login now!"}, 200

        if user.verified:
            raise BadRequest("Your account is already verified, you can log in")


class LoginUser:
    @staticmethod
    def login_user(data):
        username, password = data["username"], data["password"]
        user = AllUsers.query.filter_by(username=username).first()
        if not check_password_hash(user.password, password):
            raise BadRequest("Invalid username or password")
        if not user.verified:
            raise BadRequest("Please verify your email in order to login!")

        refresh_token, access_token = TokenManger.encode_refresh_token(user), TokenManger.encode_access_token(user)
        return {"refresh_token": refresh_token, "access_token": access_token}
