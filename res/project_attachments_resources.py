from db_models.models import ProjectAttachments, ProjectAttachmentTypes
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import or_
import uuid
import re
import os
import subprocess
from pathlib import Path
from settings import ATTACHMENTS_FOLDER


def allowed_file(extension, file_types):
    for file_type in file_types:
        if extension in file_type.filename_extensions:
            return file_type.id
    return 1


user_fields = {
    'id': fields.Integer,
    'name': fields.String(attribute=lambda x: x.last_name + ' ' + x.first_name)
}

type_fields = {
    'name': fields.String,
    'icon': fields.String
}

attachment_fields = {
    'id': fields.Integer,
    'type_id': fields.Integer,
    'project_id': fields.Integer,
    'user_id': fields.Integer,
    'file_name': fields.String,
    'file_path': fields.String,
    'file_size': fields.Integer,
    'creation_date': fields.DateTime(attribute="creation_date"),
    'text': fields.String,
    'user_ids': fields.List(fields.Integer),
    'user_data': fields.Nested(user_fields),
    'type_data': fields.Nested(type_fields)
}

parser = reqparse.RequestParser()


class ProjectAttachmentResource(Resource):
    @marshal_with(attachment_fields)
    def get(self, id):
        try:
            attachment = session.query(ProjectAttachments).filter(ProjectAttachments.id == id).first()
            if not attachment:
                abort(404, message="Attachment type {} doesn't exist".format(id))
            return attachment
        except Exception as e:
            session.rollback()
            abort(400, message="Error while getting record Attachment Type")

    def delete(self, id):
        try:
            attachment = session.query(ProjectAttachments).filter(ProjectAttachments.id == id).first()
            if not attachment:
                abort(404, message="Attachment type {} doesn't exist".format(id))
            attachment.is_removed = True
            session.add(attachment)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while deleting record Attachment Type")

    @marshal_with(attachment_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            attachment = session.query(ProjectAttachments).filter(ProjectAttachments.id == id).first()
            attachment.text = json_data['text']
            attachment.user_ids = json_data['user_ids']
            session.add(attachment)
            session.commit()
            return attachment, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while updating record Attachment Type")


class ProjectAttachmentListResource(Resource):
    @marshal_with(attachment_fields)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('project_id')
            parser.add_argument('user_id')
            args = parser.parse_args()
            if len(args) == 0:
                abort(400, message='Arguments not found')
            project_id = args['project_id']
            user_id = args['user_id']
            attachments = session.query(ProjectAttachments) \
                .filter(ProjectAttachments.project_id == project_id,
                        ProjectAttachments.is_removed == False,
                        or_(ProjectAttachments.user_id == user_id,
                            ProjectAttachments.user_ids.any(user_id))) \
                .all()
            return attachments
        except Exception as e:
            session.rollback()
            abort(400, message="Error while getting records Attachment Type")

    @marshal_with(attachment_fields)
    def post(self):
        try:
            f = request.form
            user_id = f.get('userId')
            project_id = f.get('projectId')

            files = []
            for t in request.files:
                f_list = request.files.getlist(str(t))
                for j_file in f_list:
                    files.append(j_file)

            file_types = session.query(ProjectAttachmentTypes).all()
            attachment_item = session.query(ProjectAttachments).filter(
                ProjectAttachments.project_id == project_id).first()

            if attachment_item is None:
                dir_id = str(uuid.uuid4().hex)
            else:
                dir_id = attachment_item.file_path.split('\\')[-2]

            project_folder = os.path.join(ATTACHMENTS_FOLDER, dir_id)
            response = []
            for file in files:

                if not os.path.exists(project_folder):
                    os.makedirs(project_folder)

                file_name = file.filename
                extension = Path(file_name).suffix
                file_id = str(uuid.uuid4().hex)
                result_file_name = file_id + extension
                print("Save to " + result_file_name)
                file_path = os.path.join(project_folder, result_file_name)
                file.save(file_path)
                file_size = os.path.getsize(file_path)

                type_id = allowed_file(extension, file_types)

                attachment = ProjectAttachments(project_id, user_id, file_name, file_path, file_size,
                                                type_id)
                session.add(attachment)
                session.commit()
                response.append(attachment)

            return response, 201

        except Exception as e:
            session.rollback()
            abort(400, message="Error when adding images")
