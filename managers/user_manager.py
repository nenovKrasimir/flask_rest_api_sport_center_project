import boto3
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth_manager import TokenManger, get_authentication
from models.user_register import AllUsers


class RegisterUser:
    @staticmethod
    def register_user(data):
        data['password'] = generate_password_hash(data['password'])
        user = AllUsers(**data)
        db.session.add(user)
        db.session.commit()
        email_token = TokenManger.encode_email_verify_token(user)
        ses = boto3.client(
            'ses',
            region_name='eu-north-1',
            aws_access_key_id='AKIAWWUKQSYTQPB66D7B',
            aws_secret_access_key='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'
        )
        # Extract the necessary information from the request data
        sender = 'k.nenov96@abv.bg'
        recipient = data['email']
        subject = 'Registration Successful'
        message = 'Thank you for registering!' \
                  f'Link for verifying email: http://127.0.0.1:5000/verify_email/{email_token}'

        # Send an email to the new user using the SES client
        response = ses.send_email(
            Source=sender,
            Destination={
                'ToAddresses': [recipient]
            },
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': message}}
            }
        )

    @staticmethod
    def verify_user(token):
        user_data = TokenManger.decode_email_verify_token(token)
        user = AllUsers.query.filter_by(email=user_data['email']).first()
        if not user:
            raise BadRequest("Not a valid page")

        if not user.verified:
            user.verified = True
            db.session.commit()
            return {"Success": "Your account is verified you can login now!"}, 200

        if user.verified:
            raise BadRequest("Your account is already verified, you can log in")



class LoginUser:
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
