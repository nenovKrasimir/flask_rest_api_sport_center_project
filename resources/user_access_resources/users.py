from flask import request
from flask_restful import Resource

from managers.user_access_managers.user_manager import UserManager
from models.enums import UserTypes
from schemas.request.users_schema import LoginUserSchema, RegisterUserSchema, BuySubscriptionSchema, BuyEquipmentSchema
from ultilis.decorators import validate_schema, requires_role

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
    def post(self):
        data = request.get_json()
        return user_manager.login_user(data), 200


class UserSubscription(Resource):
    @requires_role(UserTypes.user)
    @validate_schema(BuySubscriptionSchema)
    def post(self):
        data = request.get_json()
        sub_type = user_manager.buy_subscription(data)
        return {"Success": f"Subscription of type {sub_type} created"}, 201


class BuyEquipments(Resource):
    @requires_role(UserTypes.user)
    @validate_schema(BuyEquipmentSchema)
    def post(self):
        data = request.get_json()
        delivery_date = user_manager.buy_equipment(data)
        return {"success": f"Delivery expected till:{delivery_date}"}, 201
