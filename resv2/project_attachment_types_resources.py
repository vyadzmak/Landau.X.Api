from db_models.modelsv2 import ProjectAttachmentTypes
from flask_restful import fields

# PARAMS
NAME = "ProjectAttachmentTypeResource"
NAME_LIST = "ProjectAttachmentTypeListResource"
ENTITY_NAME = "Project Attachment Types"
MODEL = ProjectAttachmentTypes
ROUTE = "/v2/projectAttachmentTypes"
END_POINT = "v2-project-atttachment-types"
ROUTE_LIST = ROUTE
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'name': fields.String,
    'system_name': fields.String,
    'filename_extensions': fields.List(fields.String),
    'icon': fields.String
}