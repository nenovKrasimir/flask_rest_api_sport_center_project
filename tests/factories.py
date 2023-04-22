from factory import Factory
import factory

import config
from config import *
from db import db
from models.user_register import AllUsers
from werkzeug.security import generate_password_hash, check_password_hash
from managers.other.auth_manager import TokenManger
dir_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(dir_path, '.env'))

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


def create_info_fields_for_buying_equipment(type_equipment):
    valid_data = {'card_token': "tok_bg",
                  'contact': "+359899331198",
                  'email': "k.nenov96@abv.bg",
                  'name': "mihailovich",
                  'region': "Varna",
                  'type_equipment': type_equipment}
    return valid_data


def create_info_fields_for_buying_subscription():
    subscriber_info = {"subscriber_info": {"first_name": "Remi", "last_name": "Emilov", "identity": "1111111111"},
                       "email": "k.nenov9@abv.bg", "card_token": "tok_bg",
                       "subscription_id": "price_1MvoXSEjIKHCARBFwceAJrJ5", "region": "Varna", "phone": "+359899331198"}
    return subscriber_info

