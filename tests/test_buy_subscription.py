import json
import os
from unittest.mock import patch

import stripe
from flask_testing import TestCase

from config import create_app, TestingConfig
from db import db
from managers.other.auth_manager import TokenManger
from models.sports import ActiveSubscription, Participants
from services.payment_provider_service_stripe import StripePaymentService
from tests.data_for_helping_testing import *
from tests.factories import CreateUser, CreateCoach, CreateSport


class TestBuySubscription(TestCase):
    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        db.create_all()

        stripe.api_key = os.getenv("STRIPE_TOKEN")
        TokenManger.secret = "test_jwt_token"

        self.user = CreateUser()
        self.coach = CreateCoach()
        self.sport = CreateSport()
        self.token = TokenManger.encode_access_token(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_schemas(self):
        # All required fields missing

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {}
        resp = self.client.post("/buy_subscription", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == response_buying_subscriptions_all_schema_fields_missing

        # Subscription type field missing
        valid_data = data_buying_subscriptions
        del (valid_data["subscription_type"])
        resp = self.client.post("/buy_subscription", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': {'subscription_type': ['Missing data for required field.']}}

        # Invalid subscription type
        valid_data = data_buying_subscriptions
        valid_data["subscription_type"] = "karate"
        resp = self.client.post("/buy_subscription", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': {'subscription_type': ['Not a valid type of subscription. Valid '
                                                               'types are: boxing, swimming, fitness']}}

        # Invalid subscriber info
        valid_data = data_buying_subscriptions
        del (valid_data["subscriber_info"]["first_name"])
        resp = self.client.post("/buy_subscription", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': {'subscriber_info': ['Invalid subscriber info'],
                                         'subscription_type': ['Not a valid type of subscription. Valid '
                                                               'types are: boxing, swimming, fitness']}}

    @patch.object(StripePaymentService, 'create_customer', return_value={"id": "1"})
    @patch.object(StripePaymentService, 'create_subscription')
    def test_buying_logic(self, mock_create_subscription, mock_create_customer):
        boxing_price = "price_1MvoVmEjIKHCARBFd6Px3OdZ"

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        resp = self.client.post("/buy_subscription", headers=headers, data=json.dumps(data_buying_subscriptions), )

        assert resp.status_code == 201
        assert resp.json == {"Success": "Subscription of type boxing created"}

        # Checking if the subscription is created with valid data and added to the table
        active_subscriptions = ActiveSubscription.query.first()
        assert active_subscriptions
        assert active_subscriptions.details == boxing_price

        # Checking if participant is created with valid data and added to the table
        participant = Participants.query.first()
        assert participant
        assert participant.coach[0].model_type.name == "boxing"
        assert participant.sports[0].model_type.name == "boxing"
        assert participant.subscriptions

        mock_create_subscription.assert_called_once_with({"id": "1"}, boxing_price)
