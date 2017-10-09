from db_models.models import Documents
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
import result_models.res_model as r_m

import jsonpickle
def encode(ob):
    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False);
        #jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        json_s = jsonpickle.encode(ob, unpicklable=False)
        return json_s
    except Exception as e:
        print(str(e))
        return ""
class CellDetailsListResource(Resource):
    #@marshal_with(document_fields)
    def post(self):

        try:
            json_data = request.get_json(force=True)
            json_data = json_data["json"]
            project_id = json_data["projectId"]
            type_id = json_data["analytical_type"]
            month = json_data["month"]
            year = json_data["year"]

            docs =session.query(Documents).filter(Documents.project_id==project_id).all()
            headers = []
            result =[]
            for d in docs:

                rr = json.loads(d.data)
                try:
                    itms =rr["tableData"]["items"]
                    if (len(headers)==0):
                        headers =rr["tableData"]["headers"]
                    tb = [t for t in itms if (str(t["month"])==month and str(t["year"])==year and str(t["dataType"])==type_id)]
                    if (len(tb)>0):
                        result.append(tb)
                except Exception as e:
                    t=0

            form = r_m.FormModel(headers,result)
            yy = encode(form)
            return yy
            # file_name,file_path,file_size
            t=0
        except Exception as e:
            abort(400, message="Error while adding record Document")