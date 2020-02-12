from db_models.models import AnalyticRules,Users
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import desc
from sqlalchemy import and_
import json
import datetime
import re
import modules.json_serializator as serializator
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
    'is_default': fields.Boolean,
    'created_date': fields.DateTime,
    'data':fields.String,
    'client_id':fields.Integer,
    'client_data':fields.Nested(client_fields),
    'user_id': fields.Integer,
    'user_data': fields.Nested(user_fields)

}

f_analytic_rules_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'is_default': fields.Boolean,
    'created_date': fields.DateTime,
    #'data':fields.String,
    'client_id':fields.Integer,
    'client_data':fields.Nested(client_fields),
    'user_id': fields.Integer,
    'user_data': fields.Nested(user_fields)

}


class UserClientAnalyticRulesDefaultResource(Resource):
    @marshal_with(analytic_rules_fields)
    def get(self, id):
        user_client = session.query(Users).filter(Users.id==id).first()

        if not user_client:
            abort(404, message="User Client not found")

        client_id = user_client.client_id

        analytic_rules = session.query(AnalyticRules).filter(and_(
            AnalyticRules.client_id == client_id),
            AnalyticRules.is_default == True
        ).first()
        #analytic_rules.data = serializator.encode(analytic_rules.data)
        if not analytic_rules:
            abort(404, message="Analytic Rules not found")
        return analytic_rules

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode() # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value
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
        #analytic_rules.data = serializator.encode(analytic_rules.data)
        if not analytic_rules:
            abort(404, message="Analytic Rules not found")
        return analytic_rules


class ClientAnalyticRulesList(Resource):
    @marshal_with(f_analytic_rules_fields)
    def get(self, id):
        analytic_rules = session.query(AnalyticRules).filter(AnalyticRules.client_id == id).all()
        if not analytic_rules:
            abort(404, message="Analytic Rules not found")
        return analytic_rules


class SimpleAnalyticRulesListResource(Resource):
    @marshal_with(analytic_rules_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            json_data = json.loads(json_data)
            _rule_name = json_data['name']
            json_data = json.dumps(json_data, ensure_ascii=False)

            rule_name =_rule_name+  " (Merged rules "
            rule_name+= re.sub(r'\W+', '', str(datetime.datetime.now()))+")"

            rule_name = 'ATF Test'
            analytic_rule = AnalyticRules(rule_name,
                is_default=True,
                client_id=2,
                user_id=1,
                data=json_data)
            session.add(analytic_rule)
            session.commit()
            return analytic_rule, 201
        except Exception as e:
            abort(400, message="Error while adding record Analytic Rule")

class SimpleAnalyticRulesResource(Resource):


    @marshal_with(analytic_rules_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        json_data = json.loads(json_data)
        json_data = json.dumps(json_data, ensure_ascii=False)
        analytic_rule = session.query(AnalyticRules).filter(AnalyticRules.id == id).first()
        analytic_rule.data = json_data

        session.add(analytic_rule)
        session.commit()
        return analytic_rule, 201


class AnalyticRulesResource(Resource):
    @marshal_with(analytic_rules_fields)
    def get(self, id):
        analytic_rule = session.query(AnalyticRules).filter(AnalyticRules.id == id).first()
        #analytic_rule.data = serializator.encode(analytic_rule.data)
        if not analytic_rule:
            abort(404, message="Analytic Rules {} doesn't exist".format(id))
        return analytic_rule

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
        #json_data = json.loads(json_data)
        analytic_rule = session.query(AnalyticRules).filter(AnalyticRules.id == id).first()
        matching_is_default = [s for s in json_data if "is_default" in s]
        matching_data = [s for s in json_data if "data" in s]
        analytic_rule.name = json_data["name"]

        if (len(matching_is_default)>0):
            if (json_data["is_default"]!=None and json_data["is_default"]!=""):
                analytic_rule.is_default = json_data["is_default"]


        if (len(matching_data)):
            if (json_data["data"] != None and json_data["data"] != ""):
                analytic_rule.data = json_data["data"]

        session.add(analytic_rule)
        session.commit()
        return analytic_rule, 201


class AnalyticRulesListResource(Resource):
    @marshal_with(f_analytic_rules_fields)
    def get(self):
        analytic_rules = session.query(AnalyticRules).all()
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

