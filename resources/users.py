from flask import request
from flask_restful import Resource

from managers.user_manager import RegisterUser, LoginUser
from schemas.request.users_schema import LoginUserSchema, RegisterUserSchema
from ultilis.decorators import validate_schema


class UserRegister(Resource):
    @validate_schema(RegisterUserSchema)
    def post(self):
        data = request.get_json()
        RegisterUser.register_user(data)
        return {"Success": "We send an verification link to your email adress!"}, 201


class VerifyUser(Resource):
    def get(self, token):
        return RegisterUser.verify_user(token)


class UserLogin(Resource):
    @validate_schema(LoginUserSchema)
    def get(self):
        data = request.get_json()
        return LoginUser.login_user(data), 200
