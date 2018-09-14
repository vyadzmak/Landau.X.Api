from db_models.modelsv2 import AnalyticRules
from flask_restful import Resource, fields

# PARAMS
NAME = "AnalyticRulesResource"
NAME_LIST = "AnalyticRulesListResource"
ENTITY_NAME = "AnalyticRulesResource"
MODEL = AnalyticRules
ROUTE = "/v2/analyticsRules"
END_POINT = "v2-analytics-rules"
ROUTE_LIST = ROUTE
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

user_role_fields = {
    'name': fields.String,
    'id': fields.Integer
}

client_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name"),
    'registration_date': fields.DateTime(attribute="registration_date"),
    'registration_number': fields.String(attribute="registration_number")
}
user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'client_id': fields.Integer,
    'lock_state': fields.Boolean,
    'user_role_id': fields.Integer,
    'user_role': fields.Nested(user_role_fields),
    'client': fields.Nested(client_fields)

}
project_state_fields = {
    'id': fields.Integer,
    'name': fields.String
}

OUTPUT_FIELDS = {
    'id': fields.Integer,
    'name': fields.String,
    'is_default': fields.Boolean,
    'created_date': fields.DateTime,
    'data': fields.String,
    'client_id': fields.Integer,
    'client_data': fields.Nested(client_fields),
    'user_id': fields.Integer,
    'user_data': fields.Nested(user_fields)
}

f_analytic_rules_fields = dict(OUTPUT_FIELDS)
f_analytic_rules_fields.pop('data')

OUTPUT_FIELDS_DICT = {'get-list': f_analytic_rules_fields}


def put_data_converter(json_data):
    update_item = {}
    matching_is_default = [s for s in json_data if "is_default" in s]
    matching_data = [s for s in json_data if "data" in s]

    if (len(matching_is_default) > 0):
        if (json_data["is_default"] != None and json_data["is_default"] != ""):
            update_item["is_default"] = json_data["is_default"]

    if (len(matching_data)):
        if (json_data["data"] != None and json_data["data"] != ""):
            update_item["data"] = json_data["data"]

    return update_item
