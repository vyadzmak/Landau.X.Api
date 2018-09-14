from db_models.modelsv2 import Users, UserLogins
from db.db import session
from flask import Flask, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import base64
import modules.log_helper_module as log_module
import modules.db_helper as db_helper
from resv2.users_resources import OUTPUT_FIELDS

#PARAMS
ENTITY_NAME = "User Creation"
MODEL = Users
ROUTE ="/v2/userCreation"
END_POINT = "v2-user-creation"


class UserCreationResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(OUTPUT_FIELDS)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            entity = db_helper.add_item(MODEL, json_data)
            json_data['login_data']['user_id'] = entity.id
            password = json_data['login_data']['password']
            password = str(base64.b64encode(password.encode(encoding='utf-8')))
            json_data['login_data']['password'] = password
            db_helper.add_item(UserLogins, json_data['login_data'])
            return entity, 201
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while adding record " + ENTITY_NAME)

