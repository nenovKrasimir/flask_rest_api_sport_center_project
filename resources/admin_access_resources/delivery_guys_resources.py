from flask import request
from flask_restful import Resource

from managers.admin_access_managers.delivery_manager import DeliveryGuyManger
from models.enums import UserTypes
from schemas.request.delivery_guys_schemas import AddingDeliveryGuy, DeletingDeliveryGuy, UpdateContactDeliveryGuy
from ultilis.decorators import validate_schema, requires_role


class DeliveryGuyManipulations(Resource):
    @requires_role(UserTypes.admin)
    @validate_schema(AddingDeliveryGuy)
    def post(self):
        data = request.get_json()
        DeliveryGuyManger.adding(data)
        return {"success": "Successfully added delivery guy"}, 201

    @requires_role(UserTypes.admin)
    @validate_schema(DeletingDeliveryGuy)
    def delete(self):
        data = request.get_json()
        DeliveryGuyManger.delete(data)
        return {"success": "Successfully removed delivery guy"}, 200

    @requires_role(UserTypes.admin)
    def get(self):
        return DeliveryGuyManger.access_all(), 200

    @requires_role(UserTypes.admin)
    @validate_schema(UpdateContactDeliveryGuy)
    def put(self):
        data = request.get_json()
        delivery_guy_name = DeliveryGuyManger.update_contact(data)
        return {"success": f"Updated number of delivery_guy {delivery_guy_name}"}, 200
