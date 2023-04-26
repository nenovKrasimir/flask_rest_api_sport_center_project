import json
import os

import stripe
from flask_testing import TestCase

from config import create_app, TestingConfig
from managers.other.auth_manager import TokenManger
from tests.data_for_helping_testing import *
from tests.factories import *


class TestApp(TestCase):
    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        db.create_all()

        stripe.api_key = os.getenv("STRIPE_TOKEN")
        TokenManger.secret = "test_jwt_token"

        self.user = CreateUser()
        self.token = TokenManger.encode_access_token(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_access_required(self):
        # Not passing authorization header
        headers = {"Content-Type": "application/json"}
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(data_buying_equipments))
        assert resp.status_code == 401
        assert resp.json == {"message": "Token is missing"}

        # Invalid token
        headers = {"Content-Type": "application/json", "Authorization": "Bearer: fake_token"}
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(data_buying_equipments), )
        assert resp.status_code == 401
        assert resp.json == {"message": "Token is missing"}

    def test_admin_access_required(self):
        # test without token
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer"}
        valid_data = data_admin_access_required
        resp = self.client.post("/coach_panel", headers=headers, data=json.dumps(valid_data), )
        assert resp.json == {'message': 'Token is missing'}
        assert resp.status_code == 401

        # test with valid user access token
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        resp = self.client.post("/coach_panel", headers=headers, data=json.dumps(valid_data), )
        assert resp.json == {'message': 'You have no permission to access this page'}
        assert resp.status_code == 401

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer"}
        resp = self.client.post("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data), )
        assert resp.json == {'message': 'Token is missing'}
        assert resp.status_code == 401

        # test with valid user access token
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        resp = self.client.post("/delivery_guys_panel", headers=headers, data=json.dumps(valid_data), )
        assert resp.json == {'message': 'You have no permission to access this page'}
        assert resp.status_code == 401
