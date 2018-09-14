from db_models.modelsv2 import UserRoles
from flask_restful import fields

# PARAMS
NAME = "UserRoleResource"
NAME_LIST = "UserRoleListResource"
ENTITY_NAME = "User Roles"
MODEL = UserRoles
ROUTE = "/v2/userRole"
END_POINT = "v2-user-roles"
ROUTE_LIST = ROUTE + "s"
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'name': fields.String
}
