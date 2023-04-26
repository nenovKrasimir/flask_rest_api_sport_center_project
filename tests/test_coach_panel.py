import json

from flask_testing import TestCase

from config import create_app, TestingConfig
from db import db
from managers.other.auth_manager import TokenManger
from models.enums import UserTypes
from models.sports import Coaches
from tests.data_for_helping_testing import *
from tests.factories import CreateParticipant, CreateCoach, CreateUser, CreateSport


class TestCoachPanel(TestCase):
    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        db.create_all()

        TokenManger.secret = "test_jwt_token"

        self.user = CreateUser()
        self.user.role = UserTypes.admin
        self.coach = CreateCoach()
        self.sport = CreateSport()
        self.participant = CreateParticipant()
        self.token = TokenManger.encode_access_token(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post_method_adding_coach_schemas(self):
        # All required fields missing
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {}
        resp = self.client.post("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == response_coach_panel_all_schema_fields_missing

        # No phone field added
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = data_add_coach
        del (valid_data["phone_number"])
        resp = self.client.post("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': {'phone_number': ['Missing data for required field.']}}

        # Invalid bulgarian phone provided
        valid_data["phone_number"] = "089123"
        resp = self.client.post("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.json == {'message': {'phone_number': ['Invalid bulgarian phone number']}}

        # Coach already added
        valid_data = data_add_coach
        valid_data["phone_number"] = "+359883333334"
        valid_data["first_name"] = self.coach.first_name
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        resp = self.client.post("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': 'The coach is already added for this sport'}

        # Invalid type of coach
        valid_data = data_add_coach
        valid_data["phone_number"] = "+359883333331"
        valid_data["coach_type"] = "invalid"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        resp = self.client.post("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': 'Invalid type of coach'}

    def test_del_method_delete_coach_schemas(self):
        # All required fields missing
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {}
        resp = self.client.delete("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {
            'message': {
                'first_name': ['Missing data for required field.'],
                'id': ['Missing data for required field.'],
                'last_name': ['Missing data for required field.']
            }
        }

        # Not a valid coach id provided
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {"id": "-1", "first_name": "johnson", "last_name": "peterson"}
        resp = self.client.delete("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': 'Their is no coach with that id'}

        # id does not match the name
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {"id": f"{self.coach.id}", "first_name": "johnson", "last_name": "peterson"}
        resp = self.client.delete("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': 'First name does not match the ID'}

        # Coach has active participants
        self.coach.participants.append(self.participant)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {
            "id": f"{self.coach.id}",
            "first_name": f"{self.coach.first_name}",
            "last_name": f"{self.coach.last_name}"
        }
        resp = self.client.delete("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': 'The coach has active participants, cannot be delete it'}

    def test_put_method_update_contact_schemas(self):
        # All required fields missing
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {}
        resp = self.client.put("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {
            'message': {
                'id': ['Missing data for required field.'],
                'new_phone_number': ['Missing data for required field.']
            }
        }

        # No coach with the id
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {"id": "2", "new_phone_number": "+3598123333333"}
        resp = self.client.put("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': 'No coach with that id'}

        # Not a valid phone number
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {"id": f"{self.coach.id}", "new_phone_number": "+3598123333333"}
        resp = self.client.put("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 400
        assert resp.json == {'message': {'new_phone_number': ['Invalid bulgarian phone number']}}

    def test_get_method_logic_response(self):
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        resp = self.client.get("/coach_panel", headers=headers)
        assert resp.status_code == 200
        assert resp.json == {
            'coaches': [
                {
                    'first_name': f'{self.coach.first_name}',
                    'id': self.coach.id,
                    f"last_name": f'{self.coach.last_name}'
                }
            ]
        }

    def test_put_method_logic_update_phone_number(self):
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {"id": f"{self.coach.id}", "new_phone_number": "+359899331199"}
        resp = self.client.put("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 200
        assert resp.json == {'success': f'Updated number of trainer {self.coach.first_name}'}

        # Checking if the phone number is updated
        assert self.coach.contact == valid_data["new_phone_number"]

    def test_adding_coach(self):
        valid_data = data_add_coach
        valid_data["phone_number"] = "+359883333331"

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        resp = self.client.post("/coach_panel", headers=headers, data=json.dumps(valid_data))

        assert resp.status_code == 201
        assert resp.json == {'success': 'Successfully added coach'}

        # Check added in the coach table
        coach = Coaches.query.filter_by(contact=valid_data["phone_number"]).first()
        assert coach

        # Check added valid relationship between the same coach type and sport type
        assert coach.sport.model_type.name == valid_data["coach_type"]

    def test_del_method_logic_delete_coach(self):
        self.user.role = UserTypes.admin
        self.token = TokenManger.encode_access_token(self.user)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        valid_data = {
            "id": f"{self.coach.id}",
            "first_name": f"{self.coach.first_name}",
            "last_name": f"{self.coach.last_name}"
        }
        resp = self.client.delete("/coach_panel", headers=headers, data=json.dumps(valid_data))
        assert resp.status_code == 200
        assert resp.json == {'success': 'Successfully removed coach'}

        # Checking if the coach is successfully removed
        check_coach = Coaches.query.filter_by(id=self.coach.id).first()
        assert not check_coach
