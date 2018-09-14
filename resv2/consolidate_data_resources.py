from db_models.modelsv2 import ConsolidateDataParams
from flask_restful import Resource, fields
from modules.json_serializator import engine_encode

# PARAMS
NAME = "ConsolidateDataResource"
NAME_LIST = "ConsolidateDataListResource"
ENTITY_NAME = "ConsolidateDataParams"
MODEL = ConsolidateDataParams
ROUTE = "/v2/consolidateDataParams"
END_POINT = "v2-consolidate-data-params"
ROUTE_LIST = ROUTE
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA

OUTPUT_FIELDS = {
    'id': fields.Integer,
    'data': fields.String
}

def post_data_converter(json_data):
    return {'data': engine_encode(json_data['data'])}
