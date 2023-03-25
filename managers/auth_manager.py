import jwt
from datetime import timedelta, datetime
from jwt.exceptions import DecodeError, ExpiredSignatureError
from werkzeug.exceptions import Unauthorized
from flask_httpauth import HTTPTokenAuth
from dotenv import dotenv_values

config = (dotenv_values(".env.jwt"))


class TokenManger:
    @staticmethod
    def encode_access_token(user):
        payload = {"sub": user.id, "role": user.role.name, "exp": datetime.utcnow() + timedelta(minutes=5)}
        return jwt.encode(payload, config["ACCESS_T"])

    @staticmethod
    def encode_refresh_token(user):
        payload = {"sub": user.id, "role": user.role.name, "exp": datetime.utcnow() + timedelta(days=3)}
        return jwt.encode(payload, config["REFRESH_T"])

    @staticmethod
    def decode_access_token(token):
        try:
            return jwt.decode(token, key=config["ACCESS_T"], algorithms=["HS256"])
        except ExpiredSignatureError as ex:
            raise Unauthorized("Invalid or missing access token, please send refresh token!")
        except DecodeError as ex:
            raise Unauthorized("Invalid format, please send valid token!")

    @staticmethod
    def decode_refresh_token(token):
        try:
            return jwt.decode(token, key=config["REFRESH_T"], algorithms=["HS256"])
        except  DecodeError as ex:
            raise Unauthorized("Invalid token format, please log in again!")
        except ExpiredSignatureError as ex:
            raise Unauthorized("Your session has expired, please log in again!")


auth = HTTPTokenAuth(scheme="Bearer")


def get_authentication():
    authentication = auth.get_auth()
    if authentication:
        return authentication
    raise Unauthorized("Token is missing")