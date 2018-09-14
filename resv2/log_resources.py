from db_models.modelsv2 import Log
from flask_restful import Resource, fields

# PARAMS
NAME = "LogResource"
NAME_LIST = "LogListResource"
ENTITY_NAME = "Log"
MODEL = Log
ROUTE = "/v2/log"
END_POINT = "v2-log"
ROUTE_LIST = ROUTE
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer(attribute="id"),
    'date': fields.DateTime(attribute="date"),
    'message': fields.String(attribute="message")
}
