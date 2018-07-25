from flask_restful import Resource, abort
from flask import Flask, jsonify, request
import subprocess
from settings import ENGINE_PATH


class ProjectRecalculationResource(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)

            tt = ENGINE_PATH+str(json_data["project_id"])+" "+str(json_data["user_id"])+" 0 -3"

            subprocess.Popen(tt, shell=True)
            return {"State":"OK"}, 200
        except Exception as e:
            abort(404, message="Unable to recalculate the project")


