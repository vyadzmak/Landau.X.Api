from db_models.modelsv2 import ReportOperations
from flask_restful import Resource, fields

# PARAMS
NAME = "ReportOperationsResource"
NAME_LIST = "ReportOperationsListResource"
ENTITY_NAME = "ReportOperations"
MODEL = ReportOperations
ROUTE = "/v2/reportOperations"
END_POINT = "v2-report-operations"
ROUTE_LIST = ROUTE
END_POINT_LIST = END_POINT + "-list"
# SCHEMA FIELDS
data_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
OUTPUT_FIELDS = data_fields
