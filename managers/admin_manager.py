from schemas.response.admin_panel_response import AllCoachesResponse
from models.sports import Coaches, Sports
from db import db


class AdminManager:
    @staticmethod
    def adding_coach(data):
        first_name = data["first_name"]
        last_name = data["last_name"]
        contact = data["phone_number"]
        coach_type = data["coach_type"]
        sport = Sports.query.filter_by(model_type=data["coach_type"]).first()
        coach = Coaches(first_name=first_name, last_name=last_name, contact=contact, model_type=coach_type, sport_id=sport.id)
        sport.coaches.append(coach)

        db.session.add(coach)
        db.session.commit()

    @staticmethod
    def delete_coach(data):
        coach_id = data["id"]
        coach = Coaches.query.filter_by(id=int(coach_id)).first()
        db.session.delete(coach)
        db.session.commit()

    @staticmethod
    def access_all_coaches():
        all_coaches = db.session.query(Coaches).all()
        respond_schema = AllCoachesResponse(many=True)
        result = respond_schema.dump(all_coaches)
        return {"coaches": result}

    @staticmethod
    def update_coach_contact(data):
        coach_id = data["id"]
        coach = Coaches.query.filter_by(id=int(coach_id)).first()
        coach.contact = data["new_phone_number"]
        db.session.commit()
        return coach.first_name