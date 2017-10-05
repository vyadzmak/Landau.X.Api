from db_models.models import Log
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

log_fields = {
    'id': fields.Integer(attribute="id"),
    'date': fields.DateTime(attribute="date"),
    'message': fields.String(attribute="message")

}

class LogListResource(Resource):
    @marshal_with(log_fields)
    def get(self):
        logs = session.query(Log).all()
        return logs

    @marshal_with(log_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            log =Log(message=json_data["message"])
            session.add(log)
            session.commit()
            return log, 201
        except Exception as e:
            abort(400, message="Error while adding record Log")
