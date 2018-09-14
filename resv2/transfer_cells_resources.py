from db_models.modelsv2 import TransferCellsParams, Projects
from flask_restful import Resource, fields
from modules.json_serializator import engine_encode


# PARAMS
NAME = "TransferCellResource"
NAME_LIST = "TransferCellListResource"
ENTITY_NAME = "Transfer Cells"
MODEL = TransferCellsParams
ROUTE = "/v2/transferCell"
END_POINT = "v2-transfer-cells"
ROUTE_LIST = ROUTE + "s"
END_POINT_LIST = END_POINT + "-list"
# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
OUTPUT_FIELDS = {
    'id': fields.Integer,
    'data': fields.String,
    'project_id': fields.Integer
}


def input_data_converter(json_data):
    return {'project_id': json_data['projectId'], 'data': engine_encode(json_data['data'])}
