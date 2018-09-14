from db_models.modelsv2 import ClientTypes
from flask_restful import fields

# PARAMS
NAME = "ClientTypeResource"
NAME_LIST = "ClientTypeListResource"
ENTITY_NAME = "ClientTypes"
MODEL = ClientTypes
ROUTE = "/v2/clientType"
END_POINT = "v2-client-type"
ROUTE_LIST = ROUTE + "s"
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'name': fields.String
}
