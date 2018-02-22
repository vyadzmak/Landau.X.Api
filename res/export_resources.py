from db_models.models import DefaultAnalyticRules, AnalyticRules
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import desc
from flask import Flask, make_response
from flask import Response
import  urllib.parse as urllib

class ExportDefaultAnalyticRulesResource(Resource):

    def get(self):
        schema = session.query(DefaultAnalyticRules).first()
        content = schema.data
        response = make_response(content)
        cd = 'attachment; filename=default_schema.json'
        response.headers['Content-Disposition'] = cd
        response.mimetype = 'application/json'
        return response


class ExportAnalyticRulesResource(Resource):

    def get(self,id):
        schema = session.query(AnalyticRules).filter(AnalyticRules.id==id).first()
        content = schema.data
        response = make_response(content)
        name ="Схема ("+schema.name+")"+".json"
        t =name.encode('utf-8')
        name = t.decode("utf-8")
        name = urllib.quote(name)
        cd = 'attachment; filename='+name
        response.headers['Content-Disposition'] = cd
        response.mimetype = 'application/json'
        return response