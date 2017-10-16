from db_models.models import ProjectAnalysisLog
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json

project_analysis_log_fields = {
    'id': fields.Integer,
    'data': fields.String,
    'project_id': fields.Integer
}
import jsonpickle


def encode(ob):
    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False);
        # jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        json_s = jsonpickle.encode(ob, unpicklable=True)
        return json_s
    except Exception as e:
        print(str(e))
        return ""


class ProjectSelectAnalysisLogResource(Resource):
    @marshal_with(project_analysis_log_fields)
    def get(self, id):
        log = session.query(ProjectAnalysisLog).filter(ProjectAnalysisLog.project_id == id).first()
        if not log:
            abort(404, message="Reports not found")
        return log


class ProjectAnalysisLogResource(Resource):
    @marshal_with(project_analysis_log_fields)
    def get(self, id):
        log = session.query(ProjectAnalysisLog).filter(ProjectAnalysisLog.id == id).first()
        if not log:
            abort(404, message="Report {} doesn't exist".format(id))
        return log

    def delete(self, id):
        log = session.query(ProjectAnalysisLog).filter(ProjectAnalysisLog.id == id).first()
        if not log:
            abort(404, message="Document {} doesn't exist".format(id))
        session.delete(log)
        session.commit()
        return {}, 204

    @marshal_with(project_analysis_log_fields)
    def put(self, id):
        json_data = request.get_json(force=True)
        log = session.query(ProjectAnalysisLog).filter(ProjectAnalysisLog.id == id).first()
        #report.data = json_data["data"]
        #report.name = json_data["name"]
        session.add(log)
        session.commit()
        return log, 201


class ProjectAnalysisLogListResource(Resource):
    @marshal_with(project_analysis_log_fields)
    def get(self):
        reports = session.query(ProjectAnalysisLog).all()
        return reports

    @marshal_with(project_analysis_log_fields)
    def post(self):
        try:
            t = request
            json_data = request.get_json(force=True)
            json_data = json.loads(json_data)

            reports = ProjectAnalysisLog(projectId=json_data["projectId"],
                                  data=encode(json_data["data"]))
            session.add(reports)
            session.commit()
            return reports, 201
            # return "OK"
        except Exception as e:
            abort(400, message="Error while adding record Document")
