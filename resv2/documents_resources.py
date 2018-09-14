from db_models.modelsv2 import Documents, Projects
from flask_restful import Resource, fields
from modules.str_bytes_converter import to_str, to_bytes
import json
import base64
import zlib

# PARAMS
NAME = "DocumentResource"
NAME_LIST = "DocumentListResource"
ENTITY_NAME = "Document"
MODEL = Documents
ROUTE = "/v2/document"
END_POINT = "v2-document"
ROUTE_LIST = ROUTE + "s"
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

user_role_fields = {
    'name': fields.String,
    'id': fields.Integer
}

client_fields = {
    'id': fields.Integer(attribute='id'),
    'name': fields.String(attribute='name'),
    'registration_date': fields.DateTime(attribute='registration_date'),
    'registration_number': fields.String(attribute='registration_number')
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
document_state_fields = {
    'id': fields.Integer,
    'name': fields.String
}

# OUTPUT SCHEMA

OUTPUT_FIELDS = {
    'id': fields.Integer,
    'file_name': fields.String,
    'file_path': fields.String,
    'file_size': fields.Float,
    'created_date': fields.DateTime,
    'document_state_id': fields.Integer,
    'document_state': fields.Nested(document_state_fields),
    'user_id': fields.Integer,
    'user_data': fields.Nested(user_fields),
    'account_number': fields.String,
    'is_excluded': fields.Boolean
}


class ParseDocumentData(fields.Raw):
    def format(self, value):
        s_cmpstr = value
        s_cmpstr = s_cmpstr.replace("b'", "", 1)
        s_cmpstr = s_cmpstr.replace("'", "")
        b_cmpstr = to_bytes(s_cmpstr)
        b_cmpstr = base64.b64decode(b_cmpstr)
        dec = zlib.decompress(b_cmpstr)
        result = to_str(dec)
        return result


f_document_fields = {
    'id': fields.Integer,
    'file_name': fields.String,
    'file_path': fields.String,
    'file_size': fields.Float,
    'created_date': fields.DateTime,
    'document_state_id': fields.Integer,
    # 'document_state': fields.Nested(document_state_fields),
    'user_id': fields.Integer,
    # 'user_data': fields.Nested(user_fields),
    'data': ParseDocumentData(attribute='data')
}

OUTPUT_FIELDS_DICT = {'get': f_document_fields}


def put_data_converter(json_data):
    json_data = json.loads(json_data)
    return {
        'data': encode(json_data['data']),
        'document_state_id': json_data['document_state_id'],
        'document_type_id': json_data['document_type_id'],
    }


def post_data_converter(json_data):
    return {
        'project_id': json_data['projectId'],
        'user_id': json_data['user_id'],
        'file_name': json_data['file_name'],
        'file_path': json_data['file_path'],
        'file_size': json_data['file_size']
    }
