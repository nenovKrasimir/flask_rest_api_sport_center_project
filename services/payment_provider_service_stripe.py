import os

import stripe
from dotenv import load_dotenv
from werkzeug.exceptions import BadRequest

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class StripePaymentService:
    def __init__(self, api_key):
        stripe.api_key = api_key
        self.payment = None

    @staticmethod
    def create_subscription(customer_id, subscription_id):
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{
                    'price': subscription_id,
                }],
                payment_behavior='default_incomplete',
                expand=['latest_invoice.payment_intent']
            )
            invoice_id = subscription.latest_invoice["id"]
            invoice = stripe.Invoice.retrieve(invoice_id)
            invoice.pay()
            return subscription['id']

        except (stripe.error.CardError,
                stripe.error.RateLimitError,
                stripe.error.InvalidRequestError,
                stripe.error.AuthenticationError,
                stripe.error.APIConnectionError,
                stripe.error.StripeError) as e:
            raise BadRequest(f"{e}")

    @staticmethod
    def create_customer(email, name, source, phone, address):
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                source=source,
                phone=phone,
            )
            return customer

        except (stripe.error.RateLimitError,
                stripe.error.InvalidRequestError,
                stripe.error.AuthenticationError,
                stripe.error.APIConnectionError,
                stripe.error.StripeError) as e:
            raise BadRequest(f"{e}")

    @staticmethod
    def buy_equipments(customer_id, equipment_amount):
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=equipment_amount,
                currency="BGN",
                customer=customer_id,
                payment_method="pm_card_visa",

            )
            payment_intent.confirm()

        except (stripe.error.RateLimitError,
                stripe.error.InvalidRequestError,
                stripe.error.AuthenticationError,
                stripe.error.APIConnectionError,
                stripe.error.StripeError) as e:
            raise BadRequest(f"{e}")