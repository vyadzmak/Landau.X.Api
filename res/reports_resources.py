from db_models.models import Reports
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
report_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'data': fields.String,
    'project_id': fields.Integer

}
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
class ProjectReportResource(Resource):
    @marshal_with(report_fields)
    def get(self, id):
        report = session.query(Reports).filter(Reports.project_id == id).first()
        if not report:
            abort(404, message="Reports not found")
        return report


class ReportResource(Resource):
    @marshal_with(report_fields)
    def get(self, id):
        report = session.query(Reports).filter(Reports.id == id).first()
        if not report:
            abort(404, message="Report {} doesn't exist".format(id))
        return report

    def delete(self, id):
        report = session.query(Reports).filter(Reports.id == id).first()
        if not report:
            abort(404, message="Document {} doesn't exist".format(id))
        session.delete(report)
        session.commit()
        return {}, 204

    @marshal_with(report_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        report = session.query(Reports).filter(Reports.id == id).first()
        report.data = json_data["data"]
        report.name = json_data["name"]
        session.add(report)
        session.commit()
        return report, 201


class ReportListResource(Resource):
    @marshal_with(report_fields)
    def get(self):
        reports = session.query(Reports).all()
        return reports

    @marshal_with(report_fields)
    def post(self):
        try:

            json_data = request.get_json(force=True)
            json_data = json.loads(json_data)

            reports = Reports(projectId=json_data["projectId"],name = json_data["name"],analytic_rule_id=json_data["schemaId"],data =encode(json_data["data"]))
            session.add(reports)
            session.commit()
            return reports, 201
            #return "OK"
        except Exception as e:
            abort(400, message="Error while adding record Document")
