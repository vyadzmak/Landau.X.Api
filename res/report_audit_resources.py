from db_models.models import ReportAudit
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

