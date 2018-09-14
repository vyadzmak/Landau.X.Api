from db_models.modelsv2 import Reports
from flask_restful import Resource, fields
from modules.json_serializator import engine_encode

# PARAMS
NAME = "ReportResource"
NAME_LIST = "ReportListResource"
ENTITY_NAME = "Reports"
MODEL = Reports
ROUTE = "/v2/report"
END_POINT = "v2-reports"
ROUTE_LIST = ROUTE + "s"
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'name': fields.String,
    'data': fields.String,
    'project_id': fields.Integer
}


def name_converter(name):
    if (len(name) > 30):
        name = name[:30]
        name += "..."
    return name


def post_data_converter(json_data):
    json_data = json.loads(json_data)
    return {
        'project_id': json_data['projectId'],
        'data': engine_encode(json_data['data']),
        'name': name_converter(json_data['name']),
        'analytic_rule_id': json_data["schemaId"]
    }


def put_data_converter(json_data):
    return {'data': json_data['data'], 'name': name_converter(json_data['name'])}
