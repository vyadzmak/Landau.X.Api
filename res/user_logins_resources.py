from db_models.models import UserLogins, Log
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import and_
import base64
import  copy
import datetime
import modules.log_helper_module as log_module

user_role_fields = {
    'name': fields.String,
    'id': fields.Integer
}
user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'client_id': fields.Integer,
    'lock_state': fields.Boolean,
    'user_role_id': fields.Integer,
    'user_role': fields.Nested(user_role_fields)
}
user_login_fields = {
    'id': fields.Integer,
    'login': fields.String,
    'password': fields.String,
    'token': fields.String,
    'user_id': fields.Integer,
    'registration_date': fields.DateTime,
    'last_login_date': fields.DateTime,
    'user_data': fields.Nested(user_fields)
}


class UserAuthResource(Resource):
    @marshal_with(user_login_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            login = json_data["login"]
            password = json_data["password"]
            o_password = copy.copy(password)
            t = bytes(password, 'utf-8')
            password = str(base64.b64encode(t))
            user_login = session.query(UserLogins).filter(and_(
                UserLogins.login == login,
                UserLogins.password == password))\
                .first()
            if user_login is None:
                message = "Попытка авторизации с IP адреса " + request.remote_addr + ". Данными Login=" + login + " Password=" + o_password
                log = Log(message)
                session.add(log)
                abort(403, message="User doesn't exist")
            user_login.last_login_date = datetime.datetime.now()
            session.add(user_login)
            message = "Пользователь "+user_login.user_data.first_name+" "+user_login.user_data.last_name+" зашел в кабинет (компания " +user_login.user_data.client.name+")"
            log = Log(message)
            session.add(log)
            session.commit()
            return user_login
        except Exception as e:
            log_module.add_log("User Auth error. " + str(e))
            session.rollback()
            abort(400, message="Error Auth")


class UserLoginResource(Resource):
    @marshal_with(user_login_fields)
    def get(self, id):
        abort(403, message="Unauthorized")
        # здесь надо вставить encrypted password
        user_login = session.query(UserLogins).filter(UserLogins.id == id).first()
        if not user_login:
            abort(404, message="User doesn't exist")
        return user_login

    def delete(self, id):
        user_login = session.query(UserLogins).filter(UserLogins.id == id).first()
        if not user_login:
            abort(404, message="User Login {} doesn't exist".format(id))
        session.delete(user_login)
        session.commit()
        return {}, 204

    @marshal_with(user_login_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            user_login = session.query(UserLogins).filter(UserLogins.id == id).first()
            user_login.login = json_data['login']
            t = bytes(json_data["password"], 'utf-8')
            user_login.password = str(base64.b64encode(t))
            user_login.user_id = json_data["user_id"]

            session.add(user_login)
            session.commit()
            return user_login, 201
        except Exception as e:
            abort(500, message="Internal server error")


class UserLoginListResource(Resource):
    @marshal_with(user_login_fields)
    def get(self):
        user_logins = session.query(UserLogins).all()
        return user_logins

    @marshal_with(user_login_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            en_pass = str(base64.b64encode(json_data["password"]))
            user_login = UserLogins(login=json_data["login"], password=en_pass,
                                    user_id=json_data["user_id"])
            session.add(user_login)
            session.commit()
            return user_login, 201
        except Exception as e:
            log_module.add_log("User Login error. " + str(e))
            session.rollback()
            abort(400, message="Error while adding record User Login")
