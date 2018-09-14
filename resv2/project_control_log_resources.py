from db_models.modelsv2 import ProjectControlLog, Projects
from flask_restful import Resource, fields
from modules.json_serializator import engine_encode
from modules.db_helper import update_item
import json

# PARAMS
NAME = "ProjectControlLogResource"
NAME_LIST = "ProjectControlLogListResource"
ENTITY_NAME = "ProjectControlLog"
MODEL = ProjectControlLog
ROUTE = "/v2/projectControlLog"
END_POINT = "v2-project-control-log"
ROUTE_LIST = "/v2/projectControlLog"
END_POINT_LIST = "v2-project-control-log-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'data': fields.String,
    'project_id': fields.Integer
}


def post_data_converter(json_data):
    json_data = json.loads(json_data)
    return {
        'project_id': json_data['projectId'],
        'data': engine_encode(json_data['data'])
    }

def after_post_action(entity, json_data):
    try:
        project = update_item(Projects, {'control_log_state_id': json_data["state_id"]}, entity.project_id)
        if project is None:
           raise Exception('Unable to update project with id:{}'.format(entity.project_id))
    except Exception as e:
        raise e
