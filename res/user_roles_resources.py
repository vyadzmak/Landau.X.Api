from db_models.models import UserRoles
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort,reqparse

user_role_fields = {
    'id': fields.Integer,
    'name': fields.String
}


class UserRoleResource(Resource):
    @marshal_with(user_role_fields)
    def get(self, id):
        user_role = session.query(UserRoles).filter(UserRoles.id == id).first()
        if not user_role:
            abort(404, message="User role {} doesn't exist".format(id))
        return user_role

    def delete(self, id):
        user_role = session.query(UserRoles).filter(UserRoles.id == id).first()
        if not user_role:
            abort(404, message="User role {} doesn't exist".format(id))
        session.delete(user_role)
        session.commit()
        return {}, 204

    @marshal_with(user_role_fields)
    def put(self, id):
        json_data = request.get_json(force=True)
        user_role = session.query(UserRoles).filter(UserRoles.id == id).first()
        user_role.task =json_data['name']
        session.add(user_role)
        session.commit()
        return user_role, 201

class UserRoleListResource(Resource):
    @marshal_with(user_role_fields)
    def get(self):
        user_roles = session.query(UserRoles).all()
        return user_roles

    @marshal_with(user_role_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            user_role= UserRoles(json_data['name'])
            session.add(user_role)
            session.commit()
            return user_role, 201
        except Exception as e:
            abort(400, message="Error in adding User Role")