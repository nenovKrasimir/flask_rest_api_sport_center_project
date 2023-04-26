from flask import request
from flask_restful import Resource

from managers.admin_access_managers.coach_manager import CoachManger
from models.enums import UserTypes
from schemas.request.coach_schemas import AddingCoach, DeletingCoach, UpdateContactCoach
from ultilis.decorators import validate_schema, requires_role


class CoachManipulations(Resource):
    @requires_role(UserTypes.admin)
    @validate_schema(AddingCoach)
    def post(self):
        data = request.get_json()
        CoachManger.adding(data)
        return {"success": "Successfully added coach"}, 201

    @requires_role(UserTypes.admin)
    @validate_schema(DeletingCoach)
    def delete(self):
        data = request.get_json()
        CoachManger.delete(data)
        return {"success": "Successfully removed coach"}, 200

    @requires_role(UserTypes.admin)
    def get(self):
        return CoachManger.access_all(), 200

    @requires_role(UserTypes.admin)
    @validate_schema(UpdateContactCoach)
    def put(self):
        data = request.get_json()
        name_trainer = CoachManger.update_contact(data)
        return {"success": f"Updated number of trainer {name_trainer}"}, 200
