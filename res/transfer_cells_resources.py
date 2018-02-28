from db_models.models import TransferCellsParams
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
    'project_id': fields.Integer
}

class MakeTransferCellsResource(Resource):
    def post(self):
        try:

            json_data = request.get_json(force=True)
            json_data = json.loads(json_data)
            transfer_cell_id = json_data["id"]

            #здесь запускаем движок и переброску

            return {"State": "OK"}
        except Exception as e:
            return {"State": "Error"}


class TransferCellsResource(Resource):
    @marshal_with(transfer_cells_fields)
    def get(self, id):
        transfer_cells_params = session.query(TransferCellsParams).filter(TransferCellsParams.id == id).first()
        if not transfer_cells_params:
            abort(404, message="TransferCellsParams {} doesn't exist".format(id))
        return transfer_cells_params

class TransferCellsListResource(Resource):
    @marshal_with(transfer_cells_fields)
    def get(self):
        transfer_cells = session.query(TransferCellsParams).all()
        return transfer_cells

    @marshal_with(transfer_cells_fields)
    def post(self):
        try:

            json_data = request.get_json(force=True)
            json_data = json.loads(json_data)
            transfer_cell_params = TransferCellsParams(projectId=json_data["projectId"],data=encode(json_data["data"]))
            session.add(transfer_cell_params)
            session.commit()
            return transfer_cell_params, 201
            #return "OK"
        except Exception as e:
            abort(400, message="Error while adding transfer cells")