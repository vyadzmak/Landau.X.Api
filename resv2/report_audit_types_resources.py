from db_models.modelsv2 import ReportAuditTypes
from flask_restful import Resource, fields

# PARAMS
NAME = "ReportAuditTypesResource"
NAME_LIST = "ReportAuditTypesListResource"
ENTITY_NAME = "ReportAuditTypes"
MODEL = ReportAuditTypes
ROUTE = "/v2/reportAuditTypes"
END_POINT = "v2-report-audit-types"
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
