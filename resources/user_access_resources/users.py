from flask import request
from flask_restful import Resource

from managers.user_access_managers.user_manager import UserManager
from schemas.request.users_schema import LoginUserSchema, RegisterUserSchema, BuySubscriptionSchema, BuyEquipmentSchema
from ultilis.decorators import validate_schema

user_manager = UserManager()


class UserRegister(Resource):
    @validate_schema(RegisterUserSchema)
    def post(self):
        data = request.get_json()
        user_manager.register_user(data)
        return {"Success": "We send an verification link to your email address!"}, 201


class VerifyUser(Resource):
    def get(self, token):
        return user_manager.verify_user(token), 200


class UserLogin(Resource):
    @validate_schema(LoginUserSchema)
    def get(self):
        data = request.get_json()
        return user_manager.login_user(data), 200


class UserSubscription(Resource):
    @validate_schema(BuySubscriptionSchema)
    def post(self):
        data = request.get_json()
        user_manager.buy_subscription(data)
        return {"Success": "Subscription created"}, 201


class BuyEquipments(Resource):
    @validate_schema(BuyEquipmentSchema)
    def post(self):
        data = request.get_json()
        user_manager.buy_equipment(data)
        return {"success": "Delivery expected:"}, 201
