from db_models.modelsv2 import Clients
from flask_restful import fields

# PARAMS
NAME = "ClientResource"
NAME_LIST = "ClientListResource"
ENTITY_NAME = "Clients"
MODEL = Clients
ROUTE = "/v2/client"
END_POINT = "v2-client"
ROUTE_LIST = ROUTE + "s"
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

client_type_fields = {
    'id': fields.Integer,
    'name': fields.String
}


# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'name': fields.String,
    'registration_date': fields.DateTime,
    'registration_number': fields.String,
    'lock_state': fields.Boolean,
    'client_type_id': fields.Integer,
    'client_type': fields.Nested(client_type_fields)
}
