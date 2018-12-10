from db_models.models import Projects, ReportForms, Reports, Documents, ProjectAnalysisLog, ProjectAnalysis, \
    ProjectControlLog, TransferCellsParams, ProjectSharing, ProjectAttachments, Chats, ChatMessages
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import desc
# from socketIO_client import SocketIO, LoggingNamespace
#  import settings as app_settings
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

project_control_log_fields = {
    'id': fields.Integer,
    'data': fields.String,
    'project_id': fields.Integer
}

project_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'creation_date': fields.DateTime,
    'state_id': fields.Integer,
    'project_state': fields.Nested(project_state_fields),
    'user_id': fields.Integer,
    'user_data': fields.Nested(user_fields),
    'control_log_state_id': fields.Integer
}


class UserProjectList(Resource):
    @marshal_with(project_fields)
    def get(self, id):
        user_projects = session.query(Projects).filter(Projects.user_id == id)
        shared_projects = session.query(Projects) \
            .join(ProjectSharing, Projects.id == ProjectSharing.project_id) \
            .filter(ProjectSharing.users_ids.any(id))
        projects = user_projects.union(shared_projects).distinct().all()
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
        session.query(Documents).filter(Documents.project_id == id).delete(synchronize_session=False)
        session.commit()
        session.query(Reports).filter(Reports.project_id == id).delete(synchronize_session=False)
        session.commit()
        session.query(ReportForms).filter(ReportForms.project_id == id).delete(synchronize_session=False)
        session.commit()
        session.query(ProjectAnalysisLog).filter(ProjectAnalysisLog.project_id == id).delete(synchronize_session=False)
        session.commit()
        session.query(ProjectAnalysis).filter(ProjectAnalysis.project_id == id).delete(synchronize_session=False)
        session.commit()
        session.query(ProjectControlLog).filter(ProjectControlLog.project_id == id).delete(synchronize_session=False)
        session.commit()
        session.query(TransferCellsParams).filter(TransferCellsParams.project_id == id).delete(
            synchronize_session=False)
        session.commit()
        session.query(ProjectSharing).filter(ProjectSharing.project_id == id).delete(synchronize_session=False)
        session.commit()
        session.query(ProjectAttachments).filter(ProjectAttachments.project_id == id).delete(synchronize_session=False)
        session.commit()

        chats = session.query(Chats).filter(Chats.project_id == id).all()
        chat_ids = [x.id for x in chats]
        session.query(ChatMessages).filter(ChatMessages.chat_id.in_(chat_ids)).delete(synchronize_session=False)
        session.commit()
        for chat in chats:
            session.delete(chat)
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
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        project = session.query(Projects).filter(Projects.id == id).first()
        # project.user_id = json_data['user_id']
        project.state_id = json_data["state_id"]
        if (json_data["name"] != ""):
            project.name = json_data["name"]

        session.add(project)
        session.commit()
        # try:
        #     with SocketIO(app_settings.SOCKET_URL, 8000, LoggingNamespace) as socketIO:
        #         socketIO.emit('project_updated', str(project.user_id))
        #         socketIO.wait(seconds=0)
        # except Exception as e:
        #     return project, 201

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
            if isinstance(json_data, str):
                json_data = json.loads(json_data)
            project = Projects(userId=json_data["user_id"])
            session.add(project)
            session.commit()
            return project, 201
        except Exception as e:
            abort(400, message="Error while adding record Project")
