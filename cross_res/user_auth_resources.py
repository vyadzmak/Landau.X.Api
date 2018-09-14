from db_models.modelsv2 import UserLogins
from db.db import session
from flask import Flask, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import base64
import datetime
import modules.log_helper_module as log_module
import modules.db_helper as db_helper
from resv2.user_login_resources import OUTPUT_FIELDS

#PARAMS
ENTITY_NAME = "User Auth"
MODEL = UserLogins
ROUTE ="/v2/login"
END_POINT = "v2-user-auth"


class UserAuthResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(OUTPUT_FIELDS)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            login = json_data['login']
            password = json_data['password']
            password = str(base64.b64encode(password.encode(encoding='utf-8')))
            entity = session.query(MODEL).filter(
                MODEL.login == login,
                MODEL.password == password) \
                .first()
            if entity is None:
                message = "Попытка авторизации с IP адреса " + request.remote_addr + ". Данными Login=" + login + " Password=" + json_data['password']
                log_module.add_log(message)
                abort(403, message="User doesn't exist")
            entity.last_login_date = datetime.datetime.now()
            session.add(entity)
            session.commit()
            message = "Пользователь "+entity.user_data.first_name+" "+entity.user_data.last_name+" зашел в кабинет (компания " +entity.user_data.client.name+")"
            log_module.add_log(message)
            return entity
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            session.rollback()
            abort(400, message="Error Auth")

