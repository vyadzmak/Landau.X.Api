from db_models.modelsv2 import Users
from db.db import session
from flask import Flask, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.log_helper_module as log_module
from resv2.users_resources import OUTPUT_FIELDS

#PARAMS
ENTITY_NAME = "Users By Client"
MODEL = Users
ROUTE ="/v2/clientUsers/<int:id>"
END_POINT = "v2-users-by-client"


class ClientUsersListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(OUTPUT_FIELDS)
    def get(self, id):
        try:
            users = session.query(Users).filter(Users.client_id == id).all()
            if not users:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            return users
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting Client Users: with id:{}".format(id))

