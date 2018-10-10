from db_models.models import Log
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import or_

log_fields = {
    'id': fields.Integer(attribute="id"),
    'date': fields.DateTime(attribute="date"),
    'message': fields.String(attribute="message")
}

class LogListResource(Resource):
    @marshal_with(log_fields)
    def get(self):
        try:
            # parser = reqparse.RequestParser()
            # parser.add_argument('user_id')
            # parser.add_argument('limit')
            # parser.add_argument('last_id')
            # args = parser.parse_args()
            # limit = args.get('limit', 50000)
            # last_id = args.get('last_id', 0)
            # logs = session.query(Log).filter(or_(Log.id < last_id, last_id == '0')).order_by(Log.id.desc()).limit(limit).all()
            logs = session.query(Log).all()
            return logs
        except Exception as e:
            print(e)

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
