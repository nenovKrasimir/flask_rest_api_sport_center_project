from datetime import datetime, timedelta
import json

import stripe
from flask_testing import TestCase
from config import create_app, TestingConfig
from db import db
from tests.factories import *
from werkzeug.security import check_password_hash

from managers.other.auth_manager import TokenManger
from models.delivery_guys import Packages
from tests.data_for_helping_testing import *


class TestApp(TestCase):
    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        db.init_app(self.app)
        db.create_all()
        stripe.api_key = os.getenv("STRIPE_TOKEN")
        TokenManger.secret = "test_jwt_token"
        self.user = CreateUser()
        self.delivery_guy = CreateDeliveryGuy()
        self.token = TokenManger.encode_access_token(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_access_required(self):
        """We are going to test all the user access resources,
        We are passing no token or a wrong token only"""

        headers = {"Content-Type": "application/json"}
        valid_data = data_buying_equipments
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(valid_data), )
        assert resp.status_code == 401
        assert resp.json == {"message": "Token is missing"}

        headers = {"Content-Type": "application/json"}
        valid_data = data_buying_subscriptions
        resp = self.client.post("/buy_subscription", headers=headers, data=json.dumps(valid_data), )
        assert resp.status_code == 401
        assert resp.json == {"message": "Token is missing"}

        headers = {"Content-Type": "application/json", "Authorization": "Bearer: fake_token"}
        valid_data = data_buying_subscriptions
        resp = self.client.post("/buy_subscription", headers=headers, data=json.dumps(valid_data), )
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

    def test_buying_part(self):
        # buying equipment with valid data
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {self.token}'}
        valid_data = data_buying_equipments

        stripe.api_key = os.getenv("STRIPE_TOKEN")
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(valid_data))
        assert resp.json == {'success': f'Delivery expected till:{(datetime.utcnow() + timedelta(days=3)).date()}'}
        check_package_is_added = True if Packages.query.filter_by(recipient_contact=valid_data["contact"]).first() else None
        assert check_package_is_added

        # buying subscription with valid data
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {self.token}'}
        valid_data = data_buying_subscriptions
        stripe.api_key = os.getenv("STRIPE_TOKEN")
        resp = self.client.post("/buy_subscription", headers=headers, data=json.dumps(valid_data))
        assert resp.json == {'success': f'Delivery expected till:{(datetime.utcnow() + timedelta(days=3)).date()}'}
        check_package_is_added = True if Packages.query.filter_by(recipient_contact=valid_data["contact"]).first() else None
        assert check_package_is_added

    def test_asd(self):
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {self.token}'}
        valid_data = {}

        stripe.api_key = os.getenv("STRIPE_TOKEN")
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(valid_data))
        assert resp.json == {'success': f'Delivery expected till:{(datetime.utcnow() + timedelta(days=3)).date()}'}
        check_package_is_added = True if Packages.query.filter_by(recipient_contact=valid_data["contact"]).first() else None
        assert check_package_is_added