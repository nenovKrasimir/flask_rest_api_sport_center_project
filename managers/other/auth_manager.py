import os
from datetime import timedelta, datetime

import jwt
from dotenv import load_dotenv
from flask_httpauth import HTTPTokenAuth
from jwt.exceptions import DecodeError, ExpiredSignatureError
from werkzeug.exceptions import Unauthorized

dir_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(dir_path, '.env'))

secret_refresh_key = os.getenv("TOKEN_REFRESH_KEY")
secret_access_key = os.getenv("TOKEN_ACCESS_KEY")


class TokenManger:
    @staticmethod
    def encode_access_token(user):
        payload = {"sub": user.id, "role": user.role.name, "exp": datetime.utcnow() + timedelta(minutes=60)}
        return jwt.encode(payload, secret_access_key)

    @staticmethod
    def encode_refresh_token(user):
        payload = {"sub": user.id, "role": user.role.name, "exp": datetime.utcnow() + timedelta(days=3)}
        return jwt.encode(payload, secret_refresh_key)

    @staticmethod
    def encode_email_verify_token(user):
        payload = {"sub": user.id, "email": user.email, "exp": datetime.utcnow() + timedelta(days=1)}
        return jwt.encode(payload, secret_access_key)

    @staticmethod
    def decode_access_token(token):
        try:
            return jwt.decode(token, key=secret_access_key, algorithms=["HS256"])
        except ExpiredSignatureError as ex:
            raise Unauthorized("Invalid or missing access token!")
        except DecodeError as ex:
            raise Unauthorized("Invalid token, please send valid token!")

    @staticmethod
    def decode_refresh_token(token):
        try:
            return jwt.decode(token, key=secret_refresh_key, algorithms=["HS256"])
        except DecodeError as ex:
            raise Unauthorized("Invalid token, please log in again!")
        except ExpiredSignatureError as ex:
            raise Unauthorized("Your session has expired, please log in again!")

    @staticmethod
    def decode_email_verify_token(token):
        try:
            return jwt.decode(token, key=secret_access_key, algorithms=["HS256"])
        except DecodeError as ex:
            raise Unauthorized("Invalid token")
        except ExpiredSignatureError as ex:
            raise Unauthorized("Please register again, your register verifying took over than 1 day")


auth = HTTPTokenAuth(scheme="Bearer")


def get_authentication():
    authentication = auth.get_auth()
    if authentication:
        return authentication
    raise Unauthorized("Token is missing")
