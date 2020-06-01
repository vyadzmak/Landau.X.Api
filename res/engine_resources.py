from flask_restful import Resource, abort
from flask import Flask, jsonify, request
import subprocess
from settings import ENGINE_PATH


class ProjectRecalculationResource(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            product_id =-1
            exists = 'product_id' in json_data
            if (exists==True):
                product_id = json_data['product_id']

            if (product_id == None):
                product_id = -1
            tt = ENGINE_PATH+str(json_data["project_id"])+" "+str(json_data["user_id"])+" 3 -1"+' '+str(product_id)

            subprocess.Popen(tt, shell=True)
            return {"State":"OK"}, 200
        except Exception as e:
            abort(404, message="Unable to recalculate the project")


