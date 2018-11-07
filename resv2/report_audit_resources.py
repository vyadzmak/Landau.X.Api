from db_models.modelsv2 import ReportAudit
from flask_restful import Resource, fields
from resv2.report_audit_types_resources import data_fields as type_fields
from resv2.report_operations_resources import data_fields as operation_fields

# PARAMS
NAME = "ReportAuditResource"
NAME_LIST = "ReportAuditListResource"
ENTITY_NAME = "ReportAudit"
MODEL = ReportAudit
ROUTE = "/v2/reportAudit"
END_POINT = "v2-report-audit"
ROUTE_LIST = ROUTE
END_POINT_LIST = END_POINT + "-list"

# SCHEMA FIELDS
data_fields = {
    'id': fields.Integer(attribute="id"),
    'history_id': fields.Integer(attribute="history_id"),
    'type_id': fields.Integer(attribute="type_id"),
    'operation_id': fields.Integer(attribute="operation_id"),
    'is_system': fields.Boolean(attribute="is_system"),
    'text': fields.String(attribute="text")
}
# NESTED SCHEMA FIELDS
# operation_data = {
#     'operation_data': fields.Nested(operation_fields)
# }
# type_data = {
#     'type_data': fields.Nested(type_fields)
# }
operation = {'operation': fields.String(attribute=lambda x: x.operation_data.name if x.operation_data else "")}
type={'type': fields.String(attribute=lambda x: x.type_data.name if x.type_data else "")}
# OUTPUT SCHEMA
OUTPUT_FIELDS = {**data_fields}
