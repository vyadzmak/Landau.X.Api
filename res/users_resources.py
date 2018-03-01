from db_models.models import AnalyticRules, Clients, Users, UserLogins, Projects, Documents, ProjectControlLog, \
    ProjectAnalysisLog, Reports, ReportForms, ProjectAnalysis, TransferCellsParams
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
    'last_login_date': fields.DateTime,
}

client_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name"),
    'registration_date': fields.DateTime(attribute="registration_date"),
    'registration_number': fields.String(attribute="registration_number")

}

user_role_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'lock_state': fields.Boolean,
    'client_id': fields.Integer,
    'client': fields.Nested(client_fields),
    'user_role_id': fields.Integer,
    'user_role': fields.Nested(user_role_fields),
    'login_data': fields.Nested(user_login_fields)
}


class ClientUsersListResource(Resource):
    @marshal_with(user_fields)
    def get(self,id):
        users = session.query(Users).filter(Users.client_id==id).all()
        return users

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = session.query(Users).filter(Users.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        return user

    def delete(self, id):
        user = session.query(Users).filter(Users.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        projects = session.query(Projects).filter(Projects.user_id == user.id).all()
        for project in projects:
            docs = session.query(Documents).filter(Documents.project_id == project.id).all()
            reports = session.query(Reports).filter(Reports.project_id == project.id).all()
            reportForms = session.query(ReportForms).filter(ReportForms.project_id == project.id).all()
            logs = session.query(ProjectAnalysisLog).filter(ProjectAnalysisLog.project_id == project.id).all()
            analysis = session.query(ProjectAnalysis).filter(ProjectAnalysis.project_id == project.id).all()
            control_logs = session.query(ProjectControlLog).filter(ProjectControlLog.project_id == project.id).all()
            transfer_cells_params = session.query(TransferCellsParams).filter(
                TransferCellsParams.project_id == project.id).all()

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

            for log in control_logs:
                session.delete(log)
                session.commit()

            for transfer_cell in transfer_cells_params:
                session.delete(transfer_cell)
                session.commit()

            _project = session.query(Projects).filter(Projects.id == id).first()
            session.delete(_project)
            session.commit()
        _user_login = session.query(UserLogins).filter(UserLogins.user_id == user.id).first()
        # _user = session.query(Users).filter(Users.id == user.id).first()
        if (_user_login!=None):
            session.delete(_user_login)
            session.commit()
        session.delete(user)
        session.commit()


        #session.delete(user)
        #session.commit()
        return {}, 200

    @marshal_with(user_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        user = session.query(Users).filter(Users.id == id).first()
        user.first_name = json_data['first_name']
        user.last_name = json_data['last_name']
        #user.registration_number = json_data["registration_number"]
        user.lock_state = json_data["lock_state"]
        user.client_id = json_data["client_id"]
        user.user_role_id = json_data["user_role_id"]

        session.add(user)

        user_login = session.query(UserLogins).filter(UserLogins.user_id==id).first()
        user_login.login =json_data["login_data"]["login"]
        password = json_data["login_data"]["password"]
        user_login.password = str(base64.b64encode(password.encode(encoding='utf-8')))
        session.add(user_login)

        session.commit()
        return user, 201


class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = session.query(Users).all()
        return users

    @marshal_with(user_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            user = Users(first_name=json_data["first_name"], last_name=json_data["last_name"],
                         lock_state=json_data["lock_state"], client_id=json_data["client_id"],
                         user_role_id=json_data["user_role_id"])
            session.add(user)
            l = json_data["login_data"]
            session.commit()
            user_id = user.id
            log =l["login"]
            passw =l["password"]

            en_pass = str(base64.b64encode(bytes(passw, "utf-8")))

            login = UserLogins(log,en_pass,user_id)
            session.add(login)
            session.commit()
            return user, 201
        except Exception as e:
            abort(400, message="Error while adding record User")
