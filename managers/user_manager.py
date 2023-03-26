from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest

from db import db
from managers.auth_manager import TokenManger
from models.user_register import AllUsers


class RegisterUser:
    @staticmethod
    def register_user(data):
        data['password'] = generate_password_hash(data['password'])
        user = AllUsers(**data)
        db.session.add(user)
        db.session.commit()


class LoginUser:
    @staticmethod
    def login_user(data):
        username, password = data["username"], data["password"]
        user = AllUsers.query.filter_by(username=username).first()
        if not check_password_hash(user.password, password):
            raise BadRequest("Invalid username or password")
        refresh_token, access_token = TokenManger.encode_refresh_token(user), TokenManger.encode_access_token(user)
        return {"refresh_token": refresh_token, "access_token": access_token}
