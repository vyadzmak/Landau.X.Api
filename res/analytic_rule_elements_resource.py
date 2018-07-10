from db_models.models import TransferCellsParams,AnalyticRules, Users
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import and_
import json
import modules.log_helper_module as log

import modules.analytic_rules_parser as a_r_parser
user_login_fields = {
    'id': fields.Integer,
    'data':fields.String
}


class AnalyticRuleElementsResource(Resource):
    #@marshal_with(user_login_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            user_id = json_data["user_id"]
            sheet_id = json_data["sheet_id"]
            user_data = session.query(Users).filter(Users.id==user_id) \
                .first()
            if user_data is None:
                abort(403, message="User doesn't exist")
            client_id = user_data.client_id

            analytic_rule = session.query(AnalyticRules).filter(and_(
                AnalyticRules.is_default == True,
                AnalyticRules.client_id== client_id)) \
                .first()
            if analytic_rule is None:
                abort(403, message="Analytic Rule doesn't exist")
            #ЗДЕСЬ НЕ НАДО ОБРАЩАТЛ ВНИМАНИЯ НА ТО ЧТО ВОЗВРАЩАЕТСЯ
            return a_r_parser.parse_analytic_rules(sheet_id,analytic_rule.data)
        except Exception as e:
            session.rollback()
            log.add_log("Error: " +str(e))
            abort(400, message="Error Auth")
