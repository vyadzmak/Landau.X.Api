from db_models.modelsv2 import ReportForms
from flask_restful import Resource, fields
from modules.json_serializator import engine_encode
import json

# PARAMS
NAME = "ReportFormResource"
NAME_LIST = "ReportFormListResource"
ENTITY_NAME = "ReportForms"
MODEL = ReportForms
ROUTE = "/v2/reportForm"
END_POINT = "v2-report-forms"
ROUTE_LIST = ROUTE + "s"
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'data': fields.String,
    'project_id': fields.Integer,
    'element_number': fields.Integer,
    'period': fields.DateTime
}


def post_data_converter(json_data):
    json_data = json.loads(json_data)
    return {
        'project_id': json_data['projectId'],
        'data': engine_encode(json_data['data']),
        'element_number': name_converter(json_data['elementNumber']),
        'period': json_data["period"]
    }
