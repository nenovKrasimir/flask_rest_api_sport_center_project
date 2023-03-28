from resources.users import UserRegister, UserLogin, VerifyUser
from resources.admin_panel import AddCoach
from resources.refresh_token import RefreshToken

routes = (
    (UserRegister, "/registration"),
    (UserLogin, "/login"),
    (AddCoach, "/admin_panel"),
    (RefreshToken, "/refresh_token"),
    (VerifyUser, "/verify_email/<token>")
)