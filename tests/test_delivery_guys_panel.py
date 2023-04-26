import json

from flask_testing import TestCase

from config import create_app, TestingConfig
from db import db
from managers.other.auth_manager import TokenManger
from models.delivery_guys import DeliveryGuys
from models.enums import UserTypes
from tests.data_for_helping_testing import *
from tests.factories import CreateUser, CreateDeliveryGuy, CreatePackage


class TestDeliveryGuysPanel(TestCase):
    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        db.create_all()

        TokenManger.secret = "test_jwt_token"
        self.user = CreateUser()
        self.user.role = UserTypes.admin
        self.delivery_guy = CreateDeliveryGuy()
        self.package = CreatePackage()
        self.token = TokenManger.encode_access_token(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post_method_schemas(self):
        # All required fields missing
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {}
        resp = self.client.post("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == response_delivery_guys_panel_all_schema_fields_missing

        # No region field added
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = data_add_delivery_guy
        del (valid_data["region"])
        resp = self.client.post("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': {'region': ['Missing data for required field.']}}

        # Invalid bulgarian phone provided
        valid_data["contact"] = "089123"
        valid_data["region"] = "Varna"
        resp = self.client.post("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.json == {'message': {'contact': ['Invalid bulgarian phone number']}}

        # Invalid region provided
        valid_data["contact"] = "0899331199"
        valid_data["region"] = "Moscow"
        resp = self.client.post("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.json == {'message': {'region': ['Invalid region for delivery']}}

    def test_put_method_schemas(self):
        # All required fields missing
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {}
        resp = self.client.put("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {
            'message': {
                'id': ['Missing data for required field.'],
                'new_contact': ['Missing data for required field.']
            }
        }

        # Invalid id provided
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {"id": "5", "new_contact": "+35988993311"}
        resp = self.client.put("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': 'No delivery guy with that id'}

        # Test invalid phone provided
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {"id": f'{self.delivery_guy.id}', "new_contact": "000000"}
        resp = self.client.put("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': {'new_contact': ['Invalid bulgarian phone number']}}

    def test_delete_method_schemas(self):
        # All required fields missing
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {}
        resp = self.client.delete("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {
            'message': {
                'first_name': ['Missing data for required field.'],
                'id': ['Missing data for required field.'],
                'last_name': ['Missing data for required field.']
            }
        }

        # Not matching id provided
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {
            "id": "123",
            "first_name": f"{self.delivery_guy.first_name}",
            "last_name": f"{self.delivery_guy.last_name}"
        }
        resp = self.client.delete("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': 'Their is no delivery guy with that id'}

        # Delivery guy has active packages
        valid_data["id"] = f"{self.delivery_guy.id}"
        valid_data["first_name"] = self.delivery_guy.first_name
        resp = self.client.delete("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': 'The delivery guy has active packages, cannot be delete it'}

        # Name doesn't match the id
        valid_data["id"] = f"{self.delivery_guy.id}"
        valid_data["first_name"] = "asd"
        db.session.delete(self.package)
        self.delivery_guy.packages.pop()
        resp = self.client.delete("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': 'First name does not match the ID'}

    def test_post_method_logic_adding_delivery_guy(self):
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = data_add_delivery_guy
        resp = self.client.post("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 201
        assert resp.json == {'success': 'Successfully added delivery guy'}

        # Checking if the delivery guy is successfully added
        added_delivery_guy = DeliveryGuys.query.filter_by(first_name=valid_data["first_name"]).first()
        assert added_delivery_guy
        assert added_delivery_guy.contact == valid_data["contact"]

    def test_put_method_logic_update_contact_number(self):
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {"id": f"{self.delivery_guy.id}", "new_contact": "+359899331133"}
        resp = self.client.put("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 200
        assert resp.json == {'success': f'Updated number of delivery_guy {self.delivery_guy.first_name}'}

        # Checking if the phone number is updated
        assert self.delivery_guy.contact == valid_data["new_contact"]

    def test_delete_method_logic_delete_delivery_guy(self):
        new_delivery_guy = CreateDeliveryGuy()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        valid_data = {
            "id": f'{new_delivery_guy.id}',
            "first_name": new_delivery_guy.first_name,
            "last_name": new_delivery_guy.last_name
        }
        resp = self.client.delete("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 200
        assert resp.json == {'success': 'Successfully removed delivery guy'}

        # Check if the delivery guy is removed
        check_delivery_guy = DeliveryGuys.query.filter_by(id=new_delivery_guy.id).first()
        assert not check_delivery_guy
