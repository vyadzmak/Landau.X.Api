from db_models.models import UserLogins
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import base64
user_login_fields = {
    'id': fields.Integer,
    'login': fields.String,
    'password': fields.String,
    'token': fields.String,
    'user_id': fields.Integer,
    'registration_date': fields.DateTime,
    'last_login_date': fields.DateTime
}


class UserAuthResource(Resource):
    @marshal_with(user_login_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            login = json_data["login"]
            password = json_data["password"]
            t = bytes(password, 'utf-8')
            password =str(base64.b64encode(t))
            user_login = session.query(UserLogins).filter(
                UserLogins.login == login and UserLogins.password == password).first()
            if not user_login:
                abort(403, message="User doesn't exist")

            return user_login
        except Exception as e:
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
            t = bytes(json_data["password"],'utf-8')
            user_login.password =str(base64.b64encode(t))
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
            en_pass =str(base64.b64encode(json_data["password"]))
            user_login = UserLogins(login=json_data["login"], password=en_pass,
                                    user_id=json_data["user_id"])
            session.add(user_login)
            session.commit()
            return user_login, 201
        except Exception as e:
            abort(400, message="Error while adding record User Login")
