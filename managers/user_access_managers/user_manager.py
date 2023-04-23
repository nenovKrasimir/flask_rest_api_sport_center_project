import datetime
import os

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

from managers.other.auth_manager import TokenManger, get_authentication
from managers.other.helper_funcs import *
from models.sports import Participants
from models.user_register import AllUsers
from services.payment_provider_service_stripe import StripePaymentService
from services.simple_email_service_aws import EmailService
from ultilis.identity_hide import *
from models.delivery_guys import DeliveryGuys, Packages

dir_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(dir_path, '.env'))

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_REGION")
server_address = os.getenv("SERVER_ADDRESS")
stripe_id = os.getenv("STRIPE_TOKEN")


class UserManager:
    def __init__(self):
        self.payment_service = StripePaymentService(stripe_id)
        self.email_service = EmailService(access_key, secret_key, server_address, region_name)

    def register_user(self, data):
        data['password'] = generate_password_hash(data['password'])
        user = AllUsers(**data)
        db.session.add(user)
        db.session.commit()
        email_token = TokenManger.encode_email_verify_token(user)
        self.email_service.send_registration_confirmation_email(data["email"], email_token)

    @staticmethod
    def verify_user(token):
        user_data = TokenManger.decode_email_verify_token(token)
        user = AllUsers.query.filter_by(email=user_data['email']).first()
        if not user:
            raise BadRequest("Not a valid page")

        if user.verified:
            raise BadRequest("Your account is already verified, you can log in")

        user.verified = True
        db.session.commit()

    @staticmethod
    def login_user(data):
        username, password = data["username"], data["password"]
        user = AllUsers.query.filter_by(username=username).first()

        if not check_password_hash(user.password, password):
            raise BadRequest("Invalid username or password")

        if not user.verified:
            raise BadRequest("Please verify your email in order to login!")

        refresh_token, access_token = TokenManger.encode_refresh_token(user), TokenManger.encode_access_token(user)
        return {"refresh_token": refresh_token, "access_token": access_token}

    def buy_subscription(self, data):
        email = data["email"]
        payment = data["card_token"]
        sub_id = data["subscription_id"]
        subscriber_info = data["subscriber_info"]
        contact = data["phone"]
        region = data["region"]

        user_access_token = get_authentication()
        TokenManger.decode_access_token(user_access_token["token"])
        participant = [x for x in Participants.query if see_identity(x.identity) == subscriber_info["identity"]]

        if not participant:
            subscriber_info["identity"] = hide_identity(subscriber_info["identity"])
            participant = Participants(**subscriber_info)
        else:
            participant = participant[0]

        create_subscription(sub_id, participant)
        stripe_user_id = self.payment_service.create_customer(email, participant.first_name, payment, contact, region)
        self.payment_service.create_subscription(stripe_user_id, sub_id)

        db.session.add(participant)
        db.session.commit()

    def buy_equipment(self, customer_data):
        user_access_token = get_authentication()
        user_id = TokenManger.decode_access_token(user_access_token['token'])
        user = AllUsers.query.filter_by(id=user_id['sub']).first()

        prices = {
            "boxing_equipment": 15000,
            "fitness_equipment": 10000,
            "swimming_equipment": 9000
        }

        amount = prices[customer_data["type_equipment"]]

        customer = self.payment_service.create_customer(
            customer_data["email"], customer_data["name"], customer_data["card_token"],
            customer_data["contact"], customer_data["region"]
        )
        self.payment_service.buy_equipments(customer["id"], amount)

        payment_information = {"paid_by": user.username, "amount": amount, "currency": "BGN",
                               "created_at": datetime.utcnow(),
                               "details": customer_data["type_equipment"]}
        add_payment(payment_information)

        delivery_guy = DeliveryGuys.query.filter_by(region=customer_data["region"]).first()

        delivery_info = {
            "recipient_name": customer_data["name"],
            "recipient_region": customer_data["region"],
            "recipient_contact": customer_data["contact"],
            "expected_delivery_date": (datetime.utcnow() + timedelta(days=3)).date(),
            "delivered_by": delivery_guy.id
        }

        db.session.add(Packages(**delivery_info))
        db.session.commit()
        return delivery_info["expected_delivery_date"]
