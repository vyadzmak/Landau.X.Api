from db_models.models import ProjectAnalysis, ProjectControlLog, ReportForms
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json


class LogItems(fields.Raw):
    def format(self, value):
        if value is None or value == '':
            return {'success': 0, 'warning': 0, 'error': 0, 'info': 0, 'engine_operations': 0}
        json_ob = decode(value)
        result = {
            'success': len([x for x in json_ob if x['state_id'] == 1]),
            'warning': len([x for x in json_ob if x['state_id'] == 2]),
            'error': len([x for x in json_ob if x['state_id'] == 3]),
            'info': len([x for x in json_ob if x['state_id'] == 4]),
            'engine_operations': len([x for x in json_ob if x['state_id'] == 5])
        }
        return result


project_analysis_fields = {
    'id': fields.Integer,
    'data': fields.String,
    'project_id': fields.Integer
}

project_analysis_fields_with_log = {
    'id': fields.Integer,
    'data': fields.String,
    'project_id': fields.Integer,
    'log': LogItems(attribute='pc_data')
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


def decode(json_s):
    try:
        ob = jsonpickle.decode(json_s)
        return ob
    except Exception as e:
        print(str(e))
        return {}


class ProjectAnalysisRemover(Resource):
    def delete(self, id):
        analysis = session.query(ProjectAnalysis).filter(ProjectAnalysis.project_id == id).all()
        for analys in analysis:
            session.delete(analys)
            session.commit()

        reports = session.query(ReportForms).filter(ReportForms.project_id == id).all()

        for report in reports:
            session.delete(report)
            session.commit()

        # if not analysis:
        #     abort(404, message="Document {} doesn't exist".format(id))
        # session.delete(analysis)
        # session.commit()
        return {}, 204


class ProjectSelectAnalysisResource(Resource):
    @marshal_with(project_analysis_fields_with_log)
    def get(self, id):
        try:
            analysis = session.query(ProjectAnalysis) \
                .join(ProjectControlLog, ProjectControlLog.project_id == ProjectAnalysis.project_id) \
                .add_columns(ProjectAnalysis.id, ProjectAnalysis.project_id, ProjectAnalysis.data,
                             ProjectControlLog.id.label('pc_id'), ProjectControlLog.data.label('pc_data')) \
                .filter(ProjectAnalysis.project_id == id).first()
            if not analysis:
                abort(404, message="Reports not found")
            return {
                'id': analysis.id,
                'data': analysis.data,
                'project_id': analysis.project_id,
                'pc_data': analysis.pc_data
            }
        except Exception as e:
            abort(400, message="Error while adding record Document")


class ProjectAnalysisResource(Resource):
    @marshal_with(project_analysis_fields)
    def get(self, id):
        analysis = session.query(ProjectAnalysis).filter(ProjectAnalysis.id == id).first()
        if not analysis:
            abort(404, message="Report {} doesn't exist".format(id))
        return analysis

    def delete(self, id):
        analysis = session.query(ProjectAnalysis).filter(ProjectAnalysis.id == id).first()
        if not analysis:
            abort(404, message="Document {} doesn't exist".format(id))
        session.delete(analysis)
        session.commit()
        return {}, 204

    @marshal_with(project_analysis_fields)
    def put(self, id):
        json_data = request.get_json(force=True)
        analysis = session.query(ProjectAnalysis).filter(ProjectAnalysis.id == id).first()
        # report.data = json_data["data"]
        # report.name = json_data["name"]
        session.add(analysis)
        session.commit()
        return analysis, 201


class ProjectAnalysisListResource(Resource):
    @marshal_with(project_analysis_fields)
    def get(self):
        reports = session.query(ProjectAnalysis).all()
        return reports

    @marshal_with(project_analysis_fields)
    def post(self):
        try:
            t = request
            json_data = request.get_json(force=True)
            json_data = json.loads(json_data)

            reports = ProjectAnalysis(projectId=json_data["projectId"],
                                      data=encode(json_data["data"]))
            session.add(reports)
            session.commit()
            return reports, 201
            # return "OK"
        except Exception as e:
            abort(400, message="Error while adding record Document")
