from db_models.models import ReportAudit, ReportHistory
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json

output_fields = {
    'id': fields.Integer,
    'type_id': fields.Integer,
    'operation_id': fields.Integer,
    'history_id': fields.Integer,
    'is_system': fields.Boolean,
    'text': fields.String,
    'operation': fields.String(attribute=lambda x: x.operation_data.name if x.operation_data else ""),
    'type': fields.String(attribute=lambda x: x.type_data.name if x.type_data else "")
}

data_fields = {
    'id': fields.Integer,
    'is_system': fields.Boolean,
    'text': fields.String,
    'operation': fields.String(attribute=lambda x: x.operation_data.name if x.operation_data else ""),
    'type': fields.String(attribute=lambda x: x.type_data.name if x.type_data else ""),
    'date': fields.DateTime(attribute= lambda x: x.report_history_data.date if x.report_history_data else None)
}

class HistoryReportAuditListResource(Resource):
    @marshal_with(output_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('history_id')
        parser.add_argument('user_id')
        args = parser.parse_args()
        if len(args) == 0:
            abort(400, message='Arguments not found')
        history_id = args['history_id']
        user_id = args['user_id']
        response = session.query(ReportAudit).filter(ReportAudit.history_id == history_id).all()
        if not response:
            abort(404, message="Report History not found")
        return response


class CellReportAuditListResource(Resource):
    @marshal_with(data_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_id')
        parser.add_argument('cell_uid')
        parser.add_argument('user_id')
        args = parser.parse_args()
        if len(args) == 0:
            abort(400, message='Arguments not found')
        project_id = args['project_id']
        cell_uid = args['cell_uid']
        user_id = args['user_id']
        response = session.query(ReportAudit)\
            .join(ReportHistory)\
            .filter(ReportAudit.history_id == ReportHistory.id, ReportHistory.project_id == project_id, ReportAudit.uid == cell_uid).all()
        if not response:
            abort(404, message="Report History not found")
        return response

