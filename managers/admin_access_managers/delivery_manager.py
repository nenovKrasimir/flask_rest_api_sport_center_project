from db import db
from managers.admin_access_managers.admin_manager import AdminManager
from models.delivery_guys import DeliveryGuys
from schemas.response.admin_panel_response import AllDeliveryGuys


class DeliveryGuyManger(AdminManager):
    @staticmethod
    def adding(data):
        db.session.add(DeliveryGuys(**data))
        db.session.commit()

    @staticmethod
    def delete(data):
        db.session.delete(DeliveryGuys.query.filter_by(id=int(data["id"])).first())
        db.session.commit()

    @staticmethod
    def access_all():
        all_delivery_guys = db.session.query(DeliveryGuys).all()
        respond_schema = AllDeliveryGuys(many=True)
        result = respond_schema.dump(all_delivery_guys)
        return result

    @staticmethod
    def update_contact(data):
        delivery_guy = DeliveryGuys.query.filter_by(id=int(data["id"])).first()
        delivery_guy.contact = data["new_contact"]
        db.session.commit()
        return delivery_guy.first_name
