from flask_restful import Resource
from flask import Flask, request
from db_models.modelsv2 import TransferCellsParams, Projects

from modules.engine_module import add_job
from modules.file_saver import save_documents
import modules.db_helper as db_helper

#PARAMS
ENTITY_NAME = "Make Transfer Cells"
MODEL = TransferCellsParams
ROUTE ="/v2/makeTransferCells"
END_POINT = "v2-make-transfer-cells"

class MakeTransferCellsResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass


    def post(self):
        try:
            json_data = request.get_json(force=True)
            transfer_cell_id = json_data["id"]

            entity = db_helper.get_item(MODEL, transfer_cell_id)
            project_id = entity.project_id

            project = db_helper.update_item(Projects, {'state_id': 2}, project_id)

            user_id = project.user_id
            # здесь запускаем движок и переброску
            # здесь запускаем движок и консолидацию
            add_job(project_id, user_id, " 1 " + str(transfer_cell_id))
            return {"State": "OK"}

        except Exception as e:
            return {"State": "Error"}
