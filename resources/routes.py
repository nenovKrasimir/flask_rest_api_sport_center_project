from resources.user_access_resources.new_access_token import NewAccessToken
from resources.user_access_resources.users import UserRegister, UserLogin, VerifyUser, UserSubscription, BuyEquipments
from resources.free_resources.free_resources import GetSports, GetProducts
from resources.admin_access_resources.coach_resources import CoachManipulations
from resources.admin_access_resources.delivery_guys_resources import DeliveryGuyManipulations

routes = (
    (UserRegister, "/registration"),
    (UserLogin, "/login"),
    (VerifyUser, "/verify_email/<token>"),
    (CoachManipulations, "/coach_panel"),
    (DeliveryGuyManipulations, "/delivery_guys_panel"),
    (NewAccessToken, "/new_access_token"),
    (UserSubscription, "/buy_subscription"),
    (BuyEquipments, "/buy_equipment"),
    (GetSports, "/get_sports"),
    (GetProducts, "/get_products")
)
