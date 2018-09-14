from db_models.modelsv2 import UserLogins
from flask_restful import fields
import base64

# PARAMS
NAME = "UserLoginResource"
NAME_LIST = "UserLoginListResource"
ENTITY_NAME = "User Logins"
MODEL = UserLogins
ROUTE = "/v2/userLogin"
END_POINT = "v2-user-logins"
ROUTE_LIST = ROUTE + "s"
END_POINT_LIST = END_POINT + "-list"

# NESTED SCHEMA FIELDS
user_role_fields = {
    'name': fields.String,
    'id': fields.Integer
}
user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'client_id': fields.Integer,
    'lock_state': fields.Boolean,
    'user_role_id': fields.Integer,
    'user_role': fields.Nested(user_role_fields)
}

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'login': fields.String,
    'password': fields.String,
    'token': fields.String,
    'user_id': fields.Integer,
    'registration_date': fields.DateTime,
    'last_login_date': fields.DateTime,
    'user_data': fields.Nested(user_fields)
}

def input_data_converter(json_data):
    password = json_data['password']
    password = str(base64.b64encode(password.encode(encoding='utf-8')))
    json_data['password'] = password
    return json_data