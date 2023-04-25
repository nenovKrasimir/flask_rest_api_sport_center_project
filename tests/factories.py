import factory
from factory import Factory
from werkzeug.security import generate_password_hash

from db import db
from models.delivery_guys import DeliveryGuys
from models.enums import CoachType, SportType
from models.sports import Coaches, Sports, Participants
from models.user_register import AllUsers


class BaseFactory(Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.commit()
        return object


class CreateUser(BaseFactory):
    class Meta:
        model = AllUsers

    username = factory.Faker("first_name")
    password = generate_password_hash("abcd")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    verified = True


class CreateDeliveryGuy(BaseFactory):
    class Meta:
        model = DeliveryGuys

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    region = "Varna"
    contact = "+359899331198"


class CreateCoach(BaseFactory):
    class Meta:
        model = Coaches

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    contact = "+359883333334"
    model_type = CoachType.boxing


class CreateSport(BaseFactory):
    class Meta:
        model = Sports

    model_type = SportType.boxing


class CreateParticipant(BaseFactory):
    class Meta:
        model = Participants

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    identity = "9301021061"
