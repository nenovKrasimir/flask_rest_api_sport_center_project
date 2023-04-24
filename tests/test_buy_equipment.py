import json
from datetime import datetime, timedelta
from unittest.mock import patch

from models.delivery_guys import Packages
from services.payment_provider_service_stripe import StripePaymentService
from tests.data_for_helping_testing import *
from tests.test_application_base import TestApp
from models.one_time_payments import OneTimePayments


class TestBuyEquipment(TestApp):
    def test_schemas(self):
        # All required fields missing
        headers = {"Content-Type": "application/json"}
        valid_data = {}
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(valid_data), )
        assert resp.status_code == 400
        assert resp.json == response_buying_equipment_all_schema_fields_missing

        # Contact data missing
        valid_data = data_buying_equipments
        del (valid_data["contact"])
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(valid_data), )
        assert resp.status_code == 400
        assert resp.json == {'message': {'contact': ['Missing data for required field.']}}

        # Contact data invalid
        valid_data = data_buying_equipments
        valid_data["contact"] = "359812"
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(valid_data), )
        assert resp.status_code == 400
        assert resp.json == {'message': {'contact': ['Invalid bulgarian phone number']}}

        # Not a valid equipment
        valid_data = data_buying_equipments
        valid_data["type_equipment"] = "asd"
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(valid_data), )
        assert resp.status_code == 400
        assert resp.json == {
            'message': {
                'contact': ['Invalid bulgarian phone number'],
                'type_equipment': ['Not a valid equipment']
            }
        }

    @patch.object(StripePaymentService, 'buy_equipments')
    @patch.object(StripePaymentService, 'create_customer', return_value={"id": "1"})
    def test_buying_equipment_access(self, mock_create_customer, mock_buy_equipment):
        # Invalid or missing token check
        self.test_user_access_required("buy_equipment", data_buying_equipments)

        # Valid token provided
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(data_buying_equipments), )

        assert resp.status_code == 201
        assert resp.json == {'success': f'Delivery expected till:{(datetime.utcnow() + timedelta(days=3)).date()}'}

    @patch.object(StripePaymentService, 'buy_equipments')
    @patch.object(StripePaymentService, 'create_customer', return_value={"id": "1"})
    def test_buying_logic(self, mock_creating_customer, mock_buy_equipments):
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        amount = 15000
        customer_id = "1"
        valid_data = data_buying_equipments
        resp = self.client.post("/buy_equipment", headers=headers, data=json.dumps(valid_data), )

        assert resp.status_code == 201
        assert resp.json == {'success': f'Delivery expected till:{(datetime.utcnow() + timedelta(days=3)).date()}'}

        # Checking if the payment is added to the one time payment table
        payments_made = OneTimePayments.query.all()
        assert len(payments_made) == 1

        # Checking if the package is added to the packages table
        package_added = Packages.query.all()
        assert len(package_added) == 1

        mock_creating_customer.assert_called_once_with(valid_data['email'],
                                                       valid_data['name'],
                                                       valid_data['card_token'],
                                                       valid_data['contact'],
                                                       valid_data['region'])
        mock_buy_equipments.assert_called_once_with(customer_id, amount)