from db_models.models import Projects, ReportHistory, Reports, ReportAuditTypes, ReportOperations, ReportAudit
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse, marshal
from modules.report_audit_comparer import get_diffs
import modules.report_data_refiner as data_refiner
import json

dicts_fields = {
    'id': fields.Integer,
    'name': fields.String
}

output_fields = {
    'id': fields.Integer,
    'date': fields.DateTime,
    'data': fields.String(attribute=lambda x: data_refiner.decompress_data(x.data)),
    'project_id': fields.Integer,
    'user_id': fields.Integer
}

output_project_report_history_fields = {
    'id': fields.Integer,
    'date': fields.DateTime,
    'project_id': fields.Integer,
    'user_id': fields.Integer,
    'user_name': fields.String(attribute=lambda x: x.user_data.first_name+" "+x.user_data.last_name if x.user_data else "Cистема")
}

import jsonpickle


def encode(ob):
    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)
        # jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        json_s = jsonpickle.encode(ob, unpicklable=True)
        return json_s
    except Exception as e:
        print(str(e))
        return ""


class ProjectReportHistoryResource(Resource):
    @marshal_with(output_fields)
    def get(self, id):
        report = session.query(ReportHistory).filter(ReportHistory.project_id == id) \
            .order_by(ReportHistory.id.desc()).first()
        if not report:
            report_v0 = session.query(Reports).filter(Reports.project_id == id).first()
            compressed_data = data_refiner.compress_data(report_v0.data)
            report = ReportHistory(project_id=id,
                                   data=compressed_data,
                                   user_id=None)

            session.add(report)
            session.commit()
        return report


class ProjectReportHistoryListResource(Resource):
    @marshal_with(output_project_report_history_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_id')
        parser.add_argument('user_id')
        args = parser.parse_args()
        if len(args) == 0:
            abort(400, message='Arguments not found')
        project_id = args['project_id']
        user_id = args['user_id']
        reports = session.query(ReportHistory).filter(ReportHistory.project_id == project_id).all()
        if not reports:
            abort(404, message="Report History not found")
        return reports


class ReportHistoryResource(Resource):
    @marshal_with(output_fields)
    def get(self, id):
        report = session.query(ReportHistory).filter(ReportHistory.id == id).first()
        if not report:
            abort(404, message="Report History {} doesn't exist".format(id))
        return report

    def delete(self, id):
        report = session.query(ReportHistory).filter(ReportHistory.id == id).first()
        if not report:
            abort(404, message="Report History {} doesn't exist".format(id))
        session.delete(report)
        session.commit()
        return {}, 204

    @marshal_with(output_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        report = session.query(ReportHistory).filter(ReportHistory.id == id).first()
        report.data = json_data["data"]
        report.user_id = json_data["user_id"]
        report.project_id = json_data["project_id"]
        report.date = json_data["date"]
        session.add(report)
        session.commit()
        return report, 201


class ReportHistoryListResource(Resource):
    @marshal_with(output_fields)
    def get(self):
        reports = session.query(ReportHistory).all()
        return reports

    @marshal_with(output_fields)
    def post(self):
        try:

            json_data = request.get_json(force=True)

            previous_report = session.query(ReportHistory).filter(ReportHistory.project_id == json_data["project_id"]) \
                .order_by(ReportHistory.id.desc()).first()
            if not previous_report:
                raise Exception('Previous report has not been found! Unable to check versions.')
            previous_report_data = data_refiner.decompress_data(previous_report.data)

            # add hex keys to json_data new cells
            report_data = data_refiner.add_uids(json_data['data'])

            diffs = get_diffs(previous_report_data, report_data)
            diffs = [ReportAudit(None, diff['type_id'], diff['operation_id'], diff['is_system'], diff['text'])
                     for diff in diffs]

            # delete timestamp props and other from json json_data["data"]
            report_data = data_refiner.delete_unused_props(report_data)
            report_data = data_refiner.compress_data(report_data)

            report = ReportHistory(project_id=json_data["project_id"],
                                   data=report_data,
                                   user_id=json_data["user_id"])
            report.report_audit_data = diffs

            session.add(report)
            session.commit()
            return report, 201

        except Exception as e:
            abort(400, message="Error while adding record Report History. "+str(e))
