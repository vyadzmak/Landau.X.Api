from db_models.modelsv2 import ProjectAnalysis
from flask_restful import Resource, fields
from modules.json_serializator import engine_encode
import json


# PARAMS
NAME = "ProjectAnalysisResource"
NAME_LIST = "ProjectAnalysisListResource"
ENTITY_NAME = "Project Analysis"
MODEL = ProjectAnalysis
ROUTE = "/v2/projectAnalysis"
END_POINT = "v2-project-analysis"
ROUTE_LIST = ROUTE
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
