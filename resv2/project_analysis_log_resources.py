from db_models.modelsv2 import ProjectAnalysisLog
from flask_restful import Resource, fields
from modules.json_serializator import engine_encode
import json

# PARAMS
NAME = "ProjectAnalysisLogResource"
NAME_LIST = "ProjectAnalysisLogListResource"
ENTITY_NAME = "Project Analysis Log"
MODEL = ProjectAnalysisLog
ROUTE = "/v2/projectAnalysisLog"
END_POINT = "v2-project-analysis-log"
ROUTE_LIST = ROUTE+"s"
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'data': fields.String,
    'project_id': fields.Integer
}

def post_data_converter(json_data):
    json_data = json.loads(json_data)
    return {'data': engine_encode(json_data['data']),
            'project_id': json_data['projectId']}

