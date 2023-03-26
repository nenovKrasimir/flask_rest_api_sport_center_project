from schemas.response.admin_panel_response import AllCoachesResponse
from models.sports import SportCoach
from db import db


class AdminManager:
    @staticmethod
    def adding_coach(data):
        first_name = data["first_name"]
        last_name = data["last_name"]
        contact = data["phone_number"]
        coach_type = data["coach_type"]
        coach = SportCoach(first_name=first_name, last_name=last_name, contact=contact, type=coach_type)
        db.session.add(coach)
        db.session.commit()

    @staticmethod
    def delete_coach(data):
        coach_id = data["id"]
        coach = SportCoach.query.filter_by(id=int(coach_id)).first()
        db.session.delete(coach)
        db.session.commit()

    @staticmethod
    def access_all_coaches():
        all_coaches = db.session.query(SportCoach).all()
        respond_schema = AllCoachesResponse(many=True)
        result = respond_schema.dump(all_coaches)
        return {"coaches": result}, 200
