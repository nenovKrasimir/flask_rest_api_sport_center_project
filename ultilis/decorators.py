from functools import wraps

from flask import request
from werkzeug.exceptions import BadRequest, Unauthorized

from managers.other.auth_manager import get_authentication, TokenManger


def validate_schema(schema_name):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            schema = schema_name()
            data = request.get_json()
            errors = schema.validate(data)
            if not errors:
                return func(*args, **kwargs)
            raise BadRequest(errors)
        return wrapper
    return decorated_function


def requires_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_authentication()
            decoded_token = TokenManger.decode_access_token(token['token'])
            user_role = decoded_token["role"]
            if user_role != role.name:
                raise Unauthorized("You have no permission to access this page")
            return f(*args, **kwargs)
        return decorated_function
    return decorator
