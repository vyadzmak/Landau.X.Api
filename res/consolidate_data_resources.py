from db_models.models import ConsolidateDataParams,Projects
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
import subprocess
from pathlib import Path
from settings import ENGINE_PATH, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import jsonpickle
def encode(ob):
    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)
        #jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        json_s = jsonpickle.encode(ob, unpicklable=True)
        return json_s
    except Exception as e:
        print(str(e))
        return ""

transfer_cells_fields = {
    'id': fields.Integer,
    'data': fields.String,

}

class MakeConsolidateResource(Resource):
    def post(self):
        try:

            json_data = request.get_json(force=True)
            #json_data = json.loads(json_data)
            transfer_cell_id = json_data["id"]
            params = session.query(ConsolidateDataParams).filter(ConsolidateDataParams.id==transfer_cell_id).first()
            data= json.loads(params.data)
            p_id = data["project_ids"][0]
            project = session.query(Projects).filter(Projects.id==p_id).first()
            user_id =project.user_id
            t=0
            product_id = project.product_id

            if (product_id==None):
                product_id = -1

            #здесь запускаем движок и консолидацию
            tt = ENGINE_PATH + str(-1) + " " + str(user_id) + " 4 "+str(transfer_cell_id)+" "+str(product_id)
            # os.system(tt)
            #РАСКОММЕНТИТЬ
            subprocess.Popen(tt, shell=True)
            return {"State": "OK"}
        except Exception as e:
            return {"State": "Error"}

class ConsolidateDataResource(Resource):
    @marshal_with(transfer_cells_fields)
    def get(self, id):
        consolidate_data = session.query(ConsolidateDataParams).filter(ConsolidateDataParams.id == id).first()
        if not consolidate_data:
            abort(404, message="ConsolidateDataParams {} doesn't exist".format(id))
        return consolidate_data

class ConsolidateDataListResource(Resource):
    @marshal_with(transfer_cells_fields)
    def get(self):
        consolidate_data = session.query(ConsolidateDataParams).all()
        return consolidate_data

    @marshal_with(transfer_cells_fields)
    def post(self):
        try:

            json_data = request.get_json(force=True)
            #json_data = json.loads(json_data)
            report = ConsolidateDataParams(data=encode(json_data))
            session.add(report)
            session.commit()
            return report, 201
            #return "OK"
        except Exception as e:
            abort(400, message="Error while adding transfer cells")