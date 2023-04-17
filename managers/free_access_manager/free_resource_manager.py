from models.sports import Sports
from schemas.response.free_resource_get_sports import AllSportsResponse


class FreeResources:
    @staticmethod
    def get_available_sports():
        response_schema = AllSportsResponse(many=True)
        result = response_schema.dump(Sports.query.all())
        return result

    @staticmethod
    def get_available_products():
        return {
            "boxing": "BoxingEquipment, BoxingSubscription",
            "swimming": "SwimmingEquipment, SwimmingSubscription",
            "fitness": "FitnessEquipment, FitnessSubscription"
        }
