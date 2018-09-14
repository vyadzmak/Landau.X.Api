from db_models.modelsv2 import AnalyticRules, Users
from db.db import session
from flask import Flask, request
from flask_restful import Resource, fields, abort
from sqlalchemy import and_
import modules.log_helper_module as log

import modules.analytic_rules_parser as a_r_parser

user_login_fields = {
    'id': fields.Integer,
    'data': fields.String
}


class AnalyticRuleElementsResource(Resource):
    def __init__(self):
        self.route = "/v2/getAnalyticRuleElements"
        self.end_point = "v2-analytic-rule-elements"

    def post(self):
        try:
            json_data = request.get_json(force=True)
            user_id = json_data["user_id"]
            sheet_id = json_data["sheet_id"]
            user_data = session.query(Users).filter(Users.id == user_id) \
                .first()
            if user_data is None:
                abort(403, message="User doesn't exist")
            client_id = user_data.client_id

            analytic_rule = session.query(AnalyticRules).filter(and_(
                AnalyticRules.is_default == True,
                AnalyticRules.client_id == client_id)) \
                .first()
            if analytic_rule is None:
                abort(403, message="Analytic Rule doesn't exist")
            # ЗДЕСЬ НЕ НАДО ОБРАЩАТЬ ВНИМАНИЯ НА ТО ЧТО ВОЗВРАЩАЕТСЯ
            return a_r_parser.parse_analytic_rules(sheet_id, analytic_rule.data)
        except Exception as e:
            session.rollback()
            log.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error in route Analytic Rule Elements")
