import bcrypt
from bcrypt import hashpw, checkpw
from werkzeug.exceptions import BadRequest

from db import db
from managers.auth_manager import TokenManger
from models.user_register import AllUsers


class RegisterUser:
    @staticmethod
    def register_user(data):
        data['password'] = hashpw(data['password'], bcrypt.gensalt())
        user = AllUsers(**data)
        db.session.add(user)
        db.session.commit()


class LoginManager:
    @staticmethod
    def login_user(data):
        username, password = data["username"], data["password"]
        user = AllUsers.query.filter_by(username=username).first()
        if not checkpw(password, user.password):
            raise BadRequest("Invalid username or password")
        refresh_token, access_token = TokenManger.encode_refresh_token(user), TokenManger.encode_access_token(user)
        return {"refresh_token": refresh_token, "access_token": access_token}
