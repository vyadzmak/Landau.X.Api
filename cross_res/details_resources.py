from db_models.modelsv2 import Documents, ReportForms
from db.db import session
from flask import Flask, request
from flask_restful import Resource, abort
from sqlalchemy import and_
import modules.details_converter as details_converter
from modules.json_serializator import engine_encode
import datetime

class CellDetailsListResource(Resource):
    def __init__(self):
        self.route = "/v2/cellDetails"
        self.end_point = "v2-cell-details"
        pass

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
            #получаем тип анализа по карточкам=0 по ОСВ =1

            analysis_type =json_data["analysis_type"]
            selection_document_id=2

            if (analytical==False and analysis_type==0):
                selection_document_id=1

            if (analytical==False and analysis_type==1):
                selection_document_id=2

            if (doc_type==3):
                selection_document_id=1
            if (analytical==False):

                docs =session.query(Documents).filter(and_(
                    Documents.project_id==project_id,
                    Documents.document_type_id==selection_document_id)

                ).all()
                model = details_converter.convert_details_by_period(docs,month,year,type_id,analysis_type,project_id)

                result = engine_encode(model)
                return result
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
        except Exception as e:
            session.rollback()
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while adding record Document")