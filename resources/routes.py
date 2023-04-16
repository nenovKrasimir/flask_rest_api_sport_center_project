from resources.admin_panel import CoachActions
from resources.new_access_token import NewAccessToken
from resources.users import UserRegister, UserLogin, VerifyUser, UserSubscription, BuyEquipments
from resources.free_resources import GetSports, GetProducts

routes = (
    (UserRegister, "/registration"),
    (UserLogin, "/login"),
    (VerifyUser, "/verify_email/<token>"),
    (CoachActions, "/admin_panel"),
    (NewAccessToken, "/new_access_token"),
    (UserSubscription, "/buy_subscription"),
    (BuyEquipments, "/buy_equipment"),
    (GetSports, "/get_sports"),
    (GetProducts, "/get_products")
)
