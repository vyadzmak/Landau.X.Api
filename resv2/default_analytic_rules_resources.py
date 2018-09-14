from db_models.modelsv2 import DefaultAnalyticRules
from flask_restful import Resource, fields
from modules.json_serializator import encode
import json

# PARAMS
NAME = "DefaultAnalyticRulesResource"
NAME_LIST = "DefaultAnalyticRulesListResource"
ENTITY_NAME = "DefaultAnalyticRules"
MODEL = DefaultAnalyticRules
ROUTE = "/v2/defaultAnalyticsRules"
END_POINT = "v2-default-analytics-rules"
ROUTE_LIST = ROUTE
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA

OUTPUT_FIELDS = {
    'id': fields.Integer,
    'data': fields.String
}

OUTPUT_FIELDS_DICT = {'get': {
    'id': fields.Integer,
    'data': fields.String(attribute=lambda x: encode(x.data))
}}


def put_data_converter(json_data):
    json_data = json.loads(json_data)
    json_data = json.dumps(json_data, ensure_ascii=False)
    return {'data': json_data}


def post_data_converter(json_data):
    return {'data': json_data['data']}
