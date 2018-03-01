from db_models.models import AnalyticRules, Clients, Users, UserLogins, Projects, Documents, ProjectControlLog, \
    ProjectAnalysisLog, Reports, ReportForms, ProjectAnalysis, TransferCellsParams
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

client_type_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}

client_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'registration_date': fields.DateTime,
    'registration_number': fields.String,
    'lock_state': fields.Boolean,
    'client_type_id': fields.Integer,
    'client_type': fields.Nested(client_type_fields)
}


class ClientResource(Resource):
    @marshal_with(client_fields)
    def get(self, id):
        client = session.query(Clients).filter(Clients.id == id).first()
        if not client:
            abort(404, message="Client {} doesn't exist".format(id))
        return client

    def delete(self, id):
        client = session.query(Clients).filter(Clients.id == id).first()
        if not client:
            abort(404, message="Client type {} doesn't exist".format(id))

        client_id = client.id
        users = session.query(Users).filter(Users.client_id == client_id).all()
        # userlogins
        # users
        for user in users:
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
            _user = session.query(Users).filter(Users.id == user.id).first()
            session.delete(_user_login)
            session.commit()
            session.delete(_user)
            session.commit()
        analytic_rules = session.query(AnalyticRules).filter(AnalyticRules.client_id==client_id).all()
        for rule in analytic_rules:
            session.delete(rule)
            session.commit()
        session.delete(client)

        session.commit()
        return {}, 200

    @marshal_with(client_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        client = session.query(Clients).filter(Clients.id == id).first()
        client.name = json_data['name']
        client.registration_number = json_data["registration_number"]
        client.lock_state = json_data["lock_state"]
        client.client_type_id = json_data["client_type_id"]
        session.add(client)
        session.commit()
        return client, 201


class ClientListResource(Resource):
    @marshal_with(client_fields)
    def get(self):
        clients = session.query(Clients).all()
        return clients

    @marshal_with(client_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            client = Clients(name=json_data["name"], registration_number=json_data["registration_number"],
                             lock_state=json_data["lock_state"], client_type_id=json_data["client_type_id"])
            session.add(client)
            session.commit()
            return client, 201
        except Exception as e:
            abort(400, message="Error while adding record Client")
