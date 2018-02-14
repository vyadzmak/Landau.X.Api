from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import os
import werkzeug
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from db_models.models import Projects, Documents,Clients,Users
import uuid
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

            # for file in files:
            #     print(file.filename)
            return {"State": "OK"}
        except Exception as e:
            return {"State": "Error"}