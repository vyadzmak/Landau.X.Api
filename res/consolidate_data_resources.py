from db_models.models import ConsolidateDataParams
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json

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
            json_data = json.loads(json_data)
            transfer_cell_id = json_data["id"]

            #здесь запускаем движок и консолидацию

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