import json

from flask_testing import TestCase
from config import create_app, TestingConfig
from db import db
from tests.factories import *
from werkzeug.security import check_password_hash

from managers.other.auth_manager import TokenManger
from models.enums import UserTypes


class TestApp(TestCase):
    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_access_required(self):
        """We are going to test all the user access resources,
        We are passing no token or a wrong token only"""

        headers = {"Content-Type": "application/json"}
        valid_data = create_info_fields_for_buying_equipment("boxing_equipment")
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(valid_data), )
        assert resp.status_code == 401
        assert resp.json == {"message": "Token is missing"}

        headers = {"Content-Type": "application/json"}
        valid_data = create_info_fields_for_buying_subscription()
        resp = self.client.post("/buy_subscription", headers=headers, data=json.dumps(valid_data), )
        assert resp.status_code == 401
        assert resp.json == {"message": "Token is missing"}

        headers = {"Content-Type": "application/json", "Authorization": "Bearer: fake_token"}
        valid_data = create_info_fields_for_buying_subscription()
        resp = self.client.post("/buy_subscription", headers=headers, data=json.dumps(valid_data), )
        assert resp.status_code == 401
        assert resp.json == {"message": "Token is missing"}

    def test_admin_access_required(self):
        TokenManger.secret = "jwt_secret_key"  # I have to set it manually because its returning None value

        user = CreateUser()
        token = TokenManger.encode_access_token(user)  # Not granting access to a user type token

        # test without token
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer"}
        valid_data = {"first_name": "Georgi", "last_name": "Iordanov", "phone_number": "+359899331198",
                      "coach_type": "boxing"}
        resp = self.client.post("/coach_panel", headers=headers, data=json.dumps(valid_data), )
        assert resp.json == {'message': 'Token is missing'}
        assert resp.status_code == 401

        # test with valid user access token
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        valid_data = {"first_name": "Georgi", "last_name": "Iordanov", "phone_number": "+359899331198",
                      "coach_type": "boxing"}
        resp = self.client.post("/coach_panel", headers=headers, data=json.dumps(valid_data), )
        assert resp.json == {'message': 'You have no permission to access this page'}
        assert resp.status_code == 401

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer"}
        valid_data = {"first_name": "Georgi", "last_name": "Iordanov", "phone_number": "+359899331198",
                      "coach_type": "boxing"}
        resp = self.client.post("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data), )
        assert resp.json == {'message': 'Token is missing'}
        assert resp.status_code == 401

        # test with valid user access token
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        valid_data = {"first_name": "Georgi", "last_name": "Iordanov", "phone_number": "+359899331198",
                      "coach_type": "boxing"}
        resp = self.client.post("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data), )
        assert resp.json == {'message': 'You have no permission to access this page'}
        assert resp.status_code == 401

