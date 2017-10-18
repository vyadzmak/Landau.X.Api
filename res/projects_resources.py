from db_models.models import Projects, ReportForms,Reports,Documents, ProjectAnalysisLog, ProjectAnalysis
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import desc
import json
user_role_fields = {
    'name': fields.String,
    'id': fields.Integer
}

client_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name"),
    'registration_date': fields.DateTime(attribute="registration_date"),
    'registration_number': fields.String(attribute="registration_number")
}
user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'client_id': fields.Integer,
    'lock_state': fields.Boolean,
    'user_role_id': fields.Integer,
    'user_role': fields.Nested(user_role_fields),
    'client': fields.Nested(client_fields)

}
project_state_fields = {
    'id': fields.Integer,
    'name': fields.String
}

project_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'creation_date': fields.DateTime,
    'state_id': fields.Integer,
    'project_state': fields.Nested(project_state_fields),
    'user_id': fields.Integer,
    'user_data': fields.Nested(user_fields)

}

class UserProjectList(Resource):
    @marshal_with(project_fields)
    def get(self, id):
        projects = session.query(Projects).filter(Projects.user_id == id).all().order_by(desc(Projects.id))
        if not projects:
            abort(404, message="Projects not found")
        return projects

class ProjectResource(Resource):
    @marshal_with(project_fields)
    def get(self, id):
        project = session.query(Projects).filter(Projects.id == id).first()
        if not project:
            abort(404, message="Project {} doesn't exist".format(id))
        return project

    def delete(self, id):
        docs = session.query(Documents).filter(Documents.project_id==id).all()
        reports = session.query(Reports).filter(Reports.project_id==id).all()
        reportForms = session.query(ReportForms).filter(ReportForms.project_id==id).all()
        logs = session.query(ProjectAnalysisLog).filter(ProjectAnalysisLog.project_id==id).all()
        analysis = session.query(ProjectAnalysis).filter(ProjectAnalysis.project_id==id).all()

        for doc in docs:
            session.delete(doc)
            session.commit()

        for report in reports:
            session.delete(report)
            session.commit()

        for report_form in reportForms:
            session.delete(report_form)
            session.commit()

        for log in logs:
            session.delete(log)
            session.commit()

        for analys in analysis:
            session.delete(analys)
            session.commit()

        project = session.query(Projects).filter(Projects.id == id).first()

        if not project:
            abort(404, message="Project {} doesn't exist".format(id))
        session.delete(project)
        session.commit()
        return {}, 200

    @marshal_with(project_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        json_data = json.loads(json_data)
        project = session.query(Projects).filter(Projects.id == id).first()
        #project.user_id = json_data['user_id']
        project.state_id = json_data["state_id"]
        if (json_data["name"]!=""):
            project.name = json_data["name"]

        session.add(project)
        session.commit()
        return project, 201


class ProjectListResource(Resource):
    @marshal_with(project_fields)
    def get(self):
        projects = session.query(Projects).order_by(Projects.id.desc()).all()
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

