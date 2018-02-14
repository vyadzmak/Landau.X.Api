from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import os
import werkzeug
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from db_models.models import Projects, Documents,Clients,Users, DefaultAnalyticRules,AnalyticRules
import uuid
import json
import modules.json_serializator as j_serializator
import subprocess


class ImportDefaultAnalyticRulesResource(Resource):
    def post(self):
        try:
            f = request.form
            userId = f.get('userId')

            files = []
            for t in request.files:
                f_list = request.files.getlist(str(t))
                for j_file in f_list:
                    files.append(j_file)

            json_file = files[0]
            content =json_file.stream.read()
            data = json.loads(content)

            s_data = j_serializator.encode(data)

            default_analytic_rule = session.query(DefaultAnalyticRules).first()
            default_analytic_rule.data = s_data
            session.add(default_analytic_rule)
            session.commit()
            # for file in files:
            #     print(file.filename)
            return {"State": "OK"}
        except Exception as e:
            return {"State": "Error"}


class ImportAnalyticRulesResource(Resource):
    def post(self):
        try:
            f = request.form
            userId = f.get('userId')
            user_data = session.query(Users).filter(Users.id==userId).first()
            client_id  = user_data.client_id

            files = []
            for t in request.files:
                f_list = request.files.getlist(str(t))
                for j_file in f_list:
                    files.append(j_file)

            json_file = files[0]

            content = json_file.stream.read()
            data = json.loads(content)
            name = data["name"]

            s_data = j_serializator.encode(data)

            analityc_rules = AnalyticRules(name,False,userId,client_id,s_data)
            session.add(analityc_rules)
            session.commit()
            return {"State": "OK"}
        except Exception as e:
            return {"State": "Error"}