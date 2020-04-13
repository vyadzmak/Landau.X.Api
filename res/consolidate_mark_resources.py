from db_models.models import ConsolidateMarkData
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
import subprocess
from settings import ENGINE_PATH

console_mark_fields = {
    'data': fields.String,
}


class ConsolidateMarkResource(Resource):
    @marshal_with(console_mark_fields)
    def get(self, id):
        # добавить сортировку
        data = session.query(ConsolidateMarkData).filter(ConsolidateMarkData.project_id == id).order_by(ConsolidateMarkData.id.desc()).first()
        if not data:
            abort(404, message="Consolidate mark {} doesn't exist".format(id))
        return data

    @marshal_with(console_mark_fields)
    def put(self, id):
        is_debug =False
        json_data = request.get_json(force=True)

        #id = json_data['id']
        data = json.dumps(json_data)
        transfer_cell_id = json_data['transfer_cell_id']

        consolidate_mark = session.query(ConsolidateMarkData).filter(ConsolidateMarkData.id == id).first()

        if (not consolidate_mark):
            abort(404, error='Consolidate mark data not found')

        consolidate_mark.data = data
        session.add(consolidate_mark)
        session.commit()

        tt = ENGINE_PATH + str(consolidate_mark.project_id) + " " + str(consolidate_mark.user_id) + " 2 " + str(transfer_cell_id)
        if (is_debug==False):
            subprocess.Popen(tt, shell=True)

        return consolidate_mark, 201


class ConsolidateMarkListResource(Resource):
    @marshal_with(console_mark_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            project_id = json_data['project_id']
            user_id = json_data['user_id']
            data = json_data['data']
            consolidate_mark = ConsolidateMarkData(project_id,user_id,data)

            session.add(consolidate_mark)
            session.commit()
            data =json.loads(data)
            data['id'] = consolidate_mark.id
            data = json.dumps(data)
            consolidate_mark.data = data
            session.add(consolidate_mark)
            session.commit()



            return consolidate_mark, 201
        except Exception as e:
            abort(400, message="Error while adding record Consolidate Mark")
