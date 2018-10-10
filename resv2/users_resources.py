from db_models.modelsv2 import Users, UserLogins
from flask_restful import fields
from modules.db_helper import update_item, add_item
import base64

# PARAMS
NAME = "UserResource"
NAME_LIST = "UserListResource"
ENTITY_NAME = "Users"
MODEL = Users
ROUTE = "/v2/user"
END_POINT = "v2-users"
ROUTE_LIST = ROUTE + "s"
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

user_login_fields = {
    'id': fields.Integer,
    'login': fields.String,
    'password': fields.String,
    'token': fields.String,
    'user_id': fields.Integer,
    'registration_date': fields.DateTime,
    'last_login_date': fields.DateTime,
}

client_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name"),
    'registration_date': fields.DateTime(attribute="registration_date"),
    'registration_number': fields.String(attribute="registration_number")

}

user_role_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'lock_state': fields.Boolean,
    'client_id': fields.Integer,
    'client': fields.Nested(client_fields),
    'user_role_id': fields.Integer,
    'user_role': fields.Nested(user_role_fields),
    # 'login_data': fields.Nested(user_login_fields, attribute=lambda x: x.login_data[0] if len(x.login_data)>0 else None)
    'login_data': fields.Nested(user_login_fields)
}

def post_data_converter(json_data):
    return json_data

def after_put_action(entity, json_data):
    try:
        login = password = json_data['login_data']['password']
        if password != "":
            password = str(base64.b64encode(password.encode(encoding='utf-8')))
            json_data['login_data']['password'] = password
        else:
            json_data['login_data'].pop('password', None)
        update_item(UserLogins, json_data['login_data'], json_data['login_data']['id'])
        if login is None:
           raise Exception('Unable to update login with user_id:{}'.format(entity.id))
    except Exception as e:
        raise e