from db_models.modelsv2 import AnalyticRules, Users
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import desc
from sqlalchemy import and_
import modules.log_helper_module as log_module
from resv2.analytic_rules_resources import OUTPUT_FIELDS, f_analytic_rules_fields

class UserClientAnalyticRulesDefaultResource(Resource):
    def __init__(self):
        self.route = "/v2/analyticsRulesUserClient/<int:id>"
        self.end_point = "v2-analytic-rules-user-client"
    @marshal_with(OUTPUT_FIELDS)
    def get(self, id):
        try:
            user_client = session.query(Users).filter(Users.id==id).first()

            if not user_client:
                abort(404, message="User Client not found")

            client_id = user_client.client_id

            analytic_rules = session.query(AnalyticRules).filter(and_(
                AnalyticRules.client_id == client_id),
                AnalyticRules.is_default == True
            ).first()
            if not analytic_rules:
                abort(404, message="Analytic Rules not found")
            return analytic_rules
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting Analytic Rules with user_id:{0}, client_id:{1}".format(id, client_id))


class ClientAnalyticRulesDefaultResource(Resource):
    def __init__(self):
        self.route = "/v2/analyticsRulesDefault/<int:id>"
        self.end_point = "v2-analytic-rules-default-client"
    @marshal_with(OUTPUT_FIELDS)
    def get(self, id):
        try:
            analytic_rules = session.query(AnalyticRules).filter(and_(
                AnalyticRules.client_id == id),
                AnalyticRules.is_default == True
            ).first()
            if not analytic_rules:
                abort(404, message="Analytic Rules not found")
            return analytic_rules
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting Default Analytic Rules with client_id:{}".format(id))


class ClientAnalyticRulesList(Resource):
    def __init__(self):
        self.route = "/v2/analyticsRulesClient/<int:id>"
        self.end_point = "v2-analytic-rules-client"
    @marshal_with(f_analytic_rules_fields)
    def get(self, id):
        try:
            analytic_rules = session.query(AnalyticRules).filter(AnalyticRules.client_id == id).all()
            if not analytic_rules:
                abort(404, message="Analytic Rules not found")
            return analytic_rules
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting Analytic Rules with client_id:{}".format(id))

