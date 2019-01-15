from db_models.modelsv2 import Projects
from flask_restful import Resource, fields
from modules.json_serializator import engine_encode
import json
import threading
import modules.socket_emitter as socket_emitter

# PARAMS
NAME = "ProjectResource"
NAME_LIST = "ProjectListResource"
ENTITY_NAME = "Projects"
MODEL = Projects
ROUTE = "/v2/project"
END_POINT = "v2-projects"
ROUTE_LIST = ROUTE + "s"
END_POINT_LIST = END_POINT + "-list"

# NESTED SCHEMA FIELDS

user_role_fields = {
    'name': fields.String,
    'id': fields.Integer
}

client_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name"),
    'registration_date': fields.DateTime(attribute="registration_date"),
    'registration_number': fields.String(attribute="registration_number")
}
user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'client_id': fields.Integer,
    'lock_state': fields.Boolean,
    'user_role_id': fields.Integer,
    'user_role': fields.Nested(user_role_fields),
    'client': fields.Nested(client_fields)

}
project_state_fields = {
    'id': fields.Integer,
    'name': fields.String
}

# project_control_log_fields = {
#     'id': fields.Integer,
#     'data': fields.String,
#     'project_id': fields.Integer
# }

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'name': fields.String,
    'creation_date': fields.DateTime,
    'state_id': fields.Integer,
    'project_state': fields.Nested(project_state_fields),
    'user_id': fields.Integer,
    'user_data': fields.Nested(user_fields),
    'control_log_state_id': fields.Integer,
    'registration_number': fields.String
}


def put_data_converter(json_data):
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    result = {'state_id': json_data['state_id']}
    if json_data.get('name', '') != '':
        result['name'] = json_data.get('name')
    if 'registration_number' in json_data:
        result['registration_number'] = json_data.get('registration_number')
    return result


def post_data_converter(json_data):
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    return {'user_id': json_data['user_id']}


def after_put_action(entity, json_data):
    try:
        socket_thread = threading.Thread(target=socket_emitter.emit,
                                         args=('project_updated', str(entity.user_id)))
        socket_thread.start()
    except Exception as e:
        pass
