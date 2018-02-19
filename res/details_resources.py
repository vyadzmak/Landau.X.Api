from db_models.models import Documents,ReportForms
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
import result_models.res_model as r_m
from sqlalchemy import and_
import modules.details_converter as details_converter
import jsonpickle
import datetime
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
            doc_type = json_data["document_type"]
            analytical = json_data["analytical"]
            analytical_type = json_data["analytical_type"]
            period = json_data["period"]
            #получаем тип анализа по карточкам=0 по ОСВ =1

            analysis_type =json_data["analysis_type"]
            selection_document_id=2

            if (analytical==False and analysis_type==0):
                selection_document_id=1

            if (analytical==False):



                docs =session.query(Documents).filter(and_(
                    Documents.project_id==project_id,
                    Documents.document_type_id==selection_document_id)

                ).all()
                model = details_converter.convert_details_by_period(docs,month,year,type_id,analysis_type)


                # form = r_m.FormModel(headers,result,d_id)
                yy = encode(model)
                return yy
            else:
                analytical_type = json_data["analytical_type"]
                period = json_data["period"]
                period = datetime.datetime.strptime(period, "%Y-%m-%d %H:%M:%S")
                report_form = session.query(ReportForms).filter(and_(
                    ReportForms.project_id==project_id,
                    ReportForms.element_number==analytical_type,
                    ReportForms.period == period
                )

                ).first()
                return report_form.data
            # file_name,file_path,file_size
            t=0
        except Exception as e:
            abort(400, message="Error while adding record Document")