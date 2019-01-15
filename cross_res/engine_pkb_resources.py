from flask_restful import Resource, abort
from flask import Flask, jsonify, request
from modules.engine_module import add_job
from modules.log_helper_module import add_log

# PARAMS
ENTITY_NAME = "Engine PKB"
ROUTE = "/v2/pkbReport"
END_POINT = "v2-pkb-report"


class EnginePkbResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    def post(self):
        try:
            json_data = request.get_json(force=True)
            # add_job(json_data["project_id"], json_data["user_id"], " 3 -1")
            return {"State": "OK"}, 200
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(404, message="Unable to recalculate the project")
