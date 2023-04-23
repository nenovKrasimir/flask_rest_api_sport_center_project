from factory import Factory
import factory

import config
from config import *
from db import db
from models.user_register import AllUsers
from werkzeug.security import generate_password_hash, check_password_hash
from managers.other.auth_manager import TokenManger
from models.delivery_guys import DeliveryGuys

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

