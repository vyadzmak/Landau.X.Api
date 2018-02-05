from db_models.models import AnalyticRules
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import desc
from sqlalchemy import and_
import json
user_role_fields = {
    'name': fields.String,
    'id': fields.Integer
}

client_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name"),
    'registration_date': fields.DateTime(attribute="registration_date"),
    'registration_number': fields.String(attribute="registration_number")
}
user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'client_id': fields.Integer,
    'lock_state': fields.Boolean,
    'user_role_id': fields.Integer,
    'user_role': fields.Nested(user_role_fields),
    'client': fields.Nested(client_fields)

}
project_state_fields = {
    'id': fields.Integer,
    'name': fields.String
}

analytic_rules_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_date': fields.DateTime,
    'data':fields.String,
    'client_id':fields.Integer,
    'client_data':fields.Nested(client_fields),
    'user_id': fields.Integer,
    'user_data': fields.Nested(user_fields)

}
class ClientAnalyticRulesDefaultResource(Resource):
    @marshal_with(analytic_rules_fields)
    def get(self, id):
        # user_login = session.query(UserLogins).filter(and_(
        #     UserLogins.login == login,
        #     UserLogins.password == password)) \
        #     .first()
        #
        analytic_rules = session.query(AnalyticRules).filter(and_(
            AnalyticRules.client_id == id),
            AnalyticRules.is_default == True
        ).first()

        if not analytic_rules:
            abort(404, message="Analytic Rules not found")
        return analytic_rules


class ClientAnalyticRulesList(Resource):
    @marshal_with(analytic_rules_fields)
    def get(self, id):
        analytic_rules = session.query(AnalyticRules).filter(AnalyticRules.client_id == id).all().order_by(desc(AnalyticRules.id))
        if not analytic_rules:
            abort(404, message="Analytic Rules not found")
        return analytic_rules

class AnalyticRulesResource(Resource):
    @marshal_with(analytic_rules_fields)
    def get(self, id):
        project = session.query(AnalyticRules).filter(AnalyticRules.id == id).first()
        if not project:
            abort(404, message="Analytic Rules {} doesn't exist".format(id))
        return project

    def delete(self, id):

        analytic_rules = session.query(AnalyticRules).filter(AnalyticRules.id == id).first()

        if not analytic_rules:
            abort(404, message="Analytic Rules {} doesn't exist".format(id))
        session.delete(analytic_rules)
        session.commit()
        return {}, 200

    @marshal_with(analytic_rules_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        json_data = json.loads(json_data)
        analytic_rule = session.query(AnalyticRules).filter(AnalyticRules.id == id).first()

        analytic_rule.is_default = json_data["is_default"]
        analytic_rule.name = json_data["name"]
        analytic_rule.data = json_data["data"]

        session.add(analytic_rule)
        session.commit()
        return analytic_rule, 201


class AnalyticRulesListResource(Resource):
    @marshal_with(analytic_rules_fields)
    def get(self):
        analytic_rules = session.query(AnalyticRules).order_by(AnalyticRules.id.desc()).all()
        return analytic_rules

    @marshal_with(analytic_rules_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            analytic_rule = AnalyticRules(
                name=json_data["name"],
                is_default=json_data["is_default"],
                client_id=json_data["client_id"],
                user_id=json_data["user_id"],
                data=json_data["data"]

            )
            session.add(analytic_rule)
            session.commit()
            return analytic_rule, 201
        except Exception as e:
            abort(400, message="Error while adding record Project")

