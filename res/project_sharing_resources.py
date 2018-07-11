from db_models.models import ProjectSharing, Projects
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

import json

project_sharing_fields = {
    'id': fields.Integer,
    'project_id': fields.Integer,
    'users_ids': fields.List(fields.Integer)
}


class ProjectSharingResource(Resource):
    @marshal_with(project_sharing_fields)
    def get(self, id):
        sharing = session.query(ProjectSharing).filter(ProjectSharing.project_id == id).first()
        if not sharing:
            abort(404, message="Project sharing {} doesn't exist".format(id))
        return sharing

    @marshal_with(project_sharing_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            sharing = session.query(ProjectSharing).filter(ProjectSharing.id == id).first()
            sharing.users_ids = json_data["users_ids"]
            session.add(sharing)
            session.commit()
            return sharing, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while updating record Project Sharing")


class ProjectSharingListResource(Resource):
    @marshal_with(project_sharing_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            sharing = ProjectSharing(project_id=json_data["project_id"],
                                     users_ids=json_data["users_ids"])

            session.add(sharing)
            session.commit()
            return sharing, 201
            # return "OK"
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Project Sharing")
