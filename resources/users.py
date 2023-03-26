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
        return {"Success": "Successful registration, please login!"}, 201


class UserLogin(Resource):
    @validate_schema(LoginUserSchema)
    def post(self):
        data = request.get_json()
        return LoginUser.login_user(data), 200