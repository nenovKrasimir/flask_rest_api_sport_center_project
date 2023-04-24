from datetime import datetime, timedelta

from werkzeug.exceptions import BadRequest

from db import db
from models.one_time_payments import OneTimePayments
from models.sports import Coaches, Sports, ActiveSubscription


def get_models(type_model, model):
    """The function will extract the objects
     from my database, depending on the type"""

    models = {"coach": Coaches, "sport": Sports}

    return models[model].query.filter_by(model_type=type_model).first()


def create_subscription(sub_type, participant):
    valid_subscriptions = {
        "boxing": "price_1MvoVmEjIKHCARBFd6Px3OdZ",
        "fitness": "price_1MvoYYEjIKHCARBFXB0v86AX",
        "swimming": "price_1MvoXSEjIKHCARBFwceAJrJ5"
    }
    sub_id = valid_subscriptions[sub_type]

    # checking if the current subscription id is in the participant active subscriptions or is not valid
    if sub_id in (sub_id.details for sub_id in participant.subscriptions) or sub_type not in valid_subscriptions:
        raise BadRequest("Type of subscription already active or wrong subscription type")

    # creating and adding the new subscription (relationship many to many)
    new_subscription = ActiveSubscription(
        **{"details": sub_id, "created_at": datetime.utcnow(),
           "expiration_date": datetime.utcnow() + timedelta(days=30)})
    participant.subscriptions.append(new_subscription)

    # creating and adding the coach to the participant (relationship many to many)
    coaches = get_models(sub_type, "coach")
    participant.coach.append(coaches)

    # creating and adding the sport to the participant (relationship many to many)
    sport = get_models(sub_type, "sport")
    participant.sports.append(sport)


def add_payment(payment_information):
    new_payment = OneTimePayments(**payment_information)
    db.session.add(new_payment)
    db.session.commit()
