import boto3
from flask import jsonify


class EmailService:
    def __init__(self, access_key, secret_key, server_address, region_name='eu-north-1', ):
        self.ses = boto3.client(
            'ses',
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.sender = 'k.nenov96@abv.bg'
        self.subject = 'Registration Successful'
        self.message = f'Thank you for registering! ' \
                       f'Link for verifying email: {server_address}/verify_email/'

    def send_registration_confirmation_email(self, recipient_email, email_token):
        response = self.ses.send_email(
            Source=self.sender,
            Destination={
                'ToAddresses': [recipient_email]
            },
            Message={
                'Subject': {'Data': self.subject},
                'Body': {'Text': {'Data': self.message + email_token}}
            }
        )
