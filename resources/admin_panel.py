from flask import request
from flask_restful import Resource

from managers.admin_manager import AdminManager
from models.enums import UserTypes
from schemas.request.admin_panel_schemas import AddingCoach, DeletingCoach
from ultilis.decorators import validate_schema, requires_role


class AddCoach(Resource):
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
        return {"Succcess": "Successfully removed coach"}, 201

    @requires_role(UserTypes.admin)
    def get(self):
        AdminManager.access_all_coaches()
