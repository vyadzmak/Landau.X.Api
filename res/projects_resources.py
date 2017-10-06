from db_models.models import Projects
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

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

client_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name"),
    'registration_date': fields.DateTime(attribute="registration_date"),
    'registration_number': fields.String(attribute="registration_number")
}

project_state_fields = {
    'id':fields.Integer,
    'name':fields.String
}

project_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'creation_date': fields.DateTime,
    'project_state': fields.Nested(project_state_fields),
    'user_id': fields.Integer,
    'user': fields.Nested(user_fields)

}


class ProjectResource(Resource):
    @marshal_with(project_fields)
    def get(self, id):
        project = session.query(Projects).filter(Projects.id == id).first()
        if not project:
            abort(404, message="Project {} doesn't exist".format(id))
        return project

    def delete(self, id):
        project = session.query(Projects).filter(Projects.id == id).first()
        if not project:
            abort(404, message="Project {} doesn't exist".format(id))
        session.delete(project)
        session.commit()
        return {}, 204

    @marshal_with(project_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        project = session.query(Projects).filter(Projects.id == id).first()
        project.user_id = json_data['user_id']
        project.state_id = json_data["state_id"]
        project.name = json_data["name"]
        session.add(project)
        session.commit()
        return project, 201


class UserListResource(Resource):
    @marshal_with(project_fields)
    def get(self):
        projects = session.query(Projects).all()
        return projects

    @marshal_with(project_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            project = Projects(userId=json_data["user_id"])
            session.add(project)
            session.commit()
            return project, 201
        except Exception as e:
            abort(400, message="Error while adding record Project")
