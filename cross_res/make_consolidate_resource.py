from db_models.modelsv2 import ConsolidateDataParams, Projects
from flask_restful import Resource
import modules.db_helper as db_helper
from modules.log_helper_module import add_log
from modules.engine_module import add_job
import json


class MakeConsolidateResource(Resource):
    def __init__(self):
        self.route = "/v2/makeConsolidateData"
        self.end_point = "v2-make-consolidate-data"

    def post(self):
        try:
            json_data = request.get_json(force=True)
            transfer_cell_id = json_data["id"]
            params = db_helper.get_item(ConsolidateDataParams, transfer_cell_id)
            if params is None:
                abort(404, "Consolidate data params not found")
            data = json.loads(params.data)
            p_id = data["project_ids"][0]
            project = db_helper.get_item(Projects, p_id)
            if project is None:
                abort(404, "Project not found")
            user_id = project.user_id
            # здесь запускаем движок и консолидацию
            add_job(-1, user_id, " 2 " + str(transfer_cell_id))
            return {"State": "OK"}
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            return {"State": "Error"}
