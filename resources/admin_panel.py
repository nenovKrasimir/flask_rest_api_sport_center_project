from flask import request
from flask_restful import Resource

from managers.admin_manager import AdminManager
from models.enums import UserTypes
from schemas.request.admin_panel_schemas import AddingCoach, DeletingCoach, UpdateContactCoach
from ultilis.decorators import validate_schema, requires_role


class CoachActions(Resource):
    @requires_role(UserTypes.admin)
    @validate_schema(AddingCoach)
    def post(self):
        data = request.get_json()
        AdminManager.adding_coach(data)
        return {"Success": "Successfully added coach"}, 201

    @requires_role(UserTypes.admin)
    @validate_schema(DeletingCoach)
    def delete(self):
        data = request.get_json()
        AdminManager.delete_coach(data)
        return {"Succcess": "Successfully removed coach"}, 200

    @requires_role(UserTypes.admin)
    def get(self):
        return AdminManager.access_all_coaches(), 200

    @requires_role(UserTypes.admin)
    @validate_schema(UpdateContactCoach)
    def put(self):
        data = request.get_json()
        name_trainer = AdminManager.update_coach_contact(data)
        return {"success": f"Updated number of trainer {name_trainer}"}, 200