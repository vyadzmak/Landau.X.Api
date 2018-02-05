from db_models.models import DefaultAnalyticRules
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import desc
import modules.serializator as serializator
import json

default_analytic_rules_fields = {
    'id': fields.Integer,
    'data': fields.String

}

class DefaultAnalyticRulesResource(Resource):
    @marshal_with(default_analytic_rules_fields)
    def get(self, id):
        default_analytic_rules = session.query(DefaultAnalyticRules).filter(DefaultAnalyticRules.id == id).first()
        default_analytic_rules.data = serializator.encode(default_analytic_rules.data)
        if not default_analytic_rules:
                abort(404, message="Analytic Rules {} doesn't exist".format(id))
        return default_analytic_rules

    def delete(self, id):
        default_analytic_rules = session.query(DefaultAnalyticRules).filter(DefaultAnalyticRules.id == id).first()

        if not default_analytic_rules:
            abort(404, message="Default Analytic Rules {} doesn't exist".format(id))
        session.delete(default_analytic_rules)
        session.commit()
        return {}, 200

    @marshal_with(default_analytic_rules_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        json_data = json.loads(json_data)
        default_analytic_rules = session.query(DefaultAnalyticRules).filter(DefaultAnalyticRules.id == id).first()
        default_analytic_rules.data = json_data

        session.add(default_analytic_rules)
        session.commit()
        return default_analytic_rules, 201


class DefaultAnalyticRulesListResource(Resource):
    @marshal_with(default_analytic_rules_fields)
    def get(self):
        projects = session.query(DefaultAnalyticRules).order_by(DefaultAnalyticRules.id.desc()).all()
        return projects

    @marshal_with(default_analytic_rules_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            default_analytic_rules = DefaultAnalyticRules(data=json_data["data"])
            session.add(default_analytic_rules)
            session.commit()
            return default_analytic_rules, 201
        except Exception as e:
            abort(400, message="Error while adding record Project")

