from db_models.models import Documents
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
class CellDetailsListResource(Resource):
    #@marshal_with(document_fields)
    def post(self):

        try:
            json_data = request.get_json(force=True)
            # file_name,file_path,file_size
            t=0
        except Exception as e:
            abort(400, message="Error while adding record Document")