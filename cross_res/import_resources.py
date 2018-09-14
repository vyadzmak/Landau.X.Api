from db.db import session
from flask import Flask, request
from flask_restful import Resource
from db_models.modelsv2 import Users, DefaultAnalyticRules, AnalyticRules
import json
import modules.json_serializator as j_serializator
import modules.db_helper as db_helper
from modules.str_bytes_converter import to_str


class ImportDefaultAnalyticRulesResource(Resource):
    def __init__(self):
        self.route = "/v2/importDefaultSchema"
        self.end_point = "v2-import-default-schema"
        pass
    def post(self):
        try:
            files = [file for file in request.files.values()]
            if len(files) == 0:
                abort(404, 'Files not found')
            json_file = files[0]
            content = json_file.stream.read()
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
            session.rollback()
            return {"State": "Error"}


class ImportAnalyticRulesResource(Resource):
    def __init__(self):
        self.route = "/v2/importSchema"
        self.end_point = "v2-import-schema"
        pass
    def post(self):
        c = ""
        try:
            f = request.form
            userId = f.get('userId')
            user = db_helper.get_item(Users, userId)
            if user is None:
                abort(404, 'User with id {} not found'.format(userId))
            client_id = user.client.id

            files = [file for file in request.files.values()]
            if len(files) == 0:
                abort(404, 'Files not found')
            json_file = files[0]

            content = json_file.stream.read()
            s_cmpstr = to_str(content)
            data = json.loads(s_cmpstr)

            name = data["name"]

            s_data = j_serializator.encode(data)

            rule = db_helper.add_item(AnalyticRules, {
                'name': name,
                'is_default': False,
                'user_id': userId,
                'client_id': client_id,
                'data': s_data
            })
            if rule is None:
                abort(400, message='Unable to add anaytic rule')
            return {"State": "OK"}
        except Exception as e:
            s = "Error: " + str(e)
            return {"State": s + "; content: " + c}
