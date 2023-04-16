from flask_restful import Resource

from managers.free_resource_manager import FreeResources


class GetSports(Resource):
    def get(self):
        return FreeResources.get_available_sports(), 200


class GetProducts(Resource):
    def get(self):
        return FreeResources.get_available_products(), 200
