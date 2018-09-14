from db_models.modelsv2 import ProjectAttachments, ProjectAttachmentTypes, ProjectSharing, Users
from db.db import session
from flask import request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import or_
import modules.db_helper as db_helper
from modules.file_saver import save_attachments

import json

# PARAMS
ENTITY_NAME = "Project Attachments"
MODEL = ProjectAttachments
ROUTE = "/v2/projectAttachments"
END_POINT = "v2-project-attachments"


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
    def __init__(self):
        self.route = ROUTE + "/<int:id>"
        self.end_point = END_POINT
        pass

    @marshal_with(attachment_fields)
    def get(self, id):
        try:
            attachment = db_helper.get_item(MODEL, id)
            if not attachment:
                abort(404, message="Attachment type {} doesn't exist".format(id))
            return attachment
        except Exception as e:
            abort(400, message="Error while getting record Attachment Type")

    def delete(self, id):
        try:
            attachment = db_helper.update_item(MODEL, {'is_removed': True}, id)
            if not attachment:
                abort(404, message="Attachment type {} doesn't exist".format(id))
            return {}, 204
        except Exception as e:
            abort(400, message="Error while deleting record Attachment Type")

    @marshal_with(attachment_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            attachment = session.query(MODEL).filter(MODEL.id == id).first()
            user_ids = set(json_data['user_ids'])
            if attachment is not None:
                project_sharing = session.query(ProjectSharing).filter(
                    ProjectSharing.project_id == attachment.project_id).first()
                if project_sharing is not None:
                    risks = session.query(Users).filter(Users.id.in_(project_sharing.users_ids),
                                                        Users.user_role_id == 7).all()
                    user_ids |= set(x.id for x in risks or [])

            attachment.text = json_data['text']
            attachment.user_ids = list(user_ids)
            session.add(attachment)
            session.commit()
            return attachment, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while updating record Attachment Type")


class ProjectAttachmentListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT + "-list"
        pass

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
            attachments = session.query(MODEL) \
                .filter(MODEL.project_id == project_id,
                        MODEL.is_removed == False,
                        or_(MODEL.user_id == user_id,
                            MODEL.user_ids.any(user_id))) \
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
            user_ids = []
            project_sharing = session.query(ProjectSharing).filter(
                ProjectSharing.project_id == project_id).first()
            if project_sharing is not None:
                risks = session.query(Users).filter(Users.id.in_(project_sharing.users_ids),
                                                    Users.user_role_id == 7).all()
                if risks is not None:
                    user_ids = [x.id for x in risks]

            file_types = db_helper.get_items(ProjectAttachmentTypes)
            attachment_item = session.query(MODEL).filter(
                MODEL.project_id == project_id).first()
            if attachment_item is None:
                files = save_attachments(request.files)
            else:
                files = save_attachments(request.files, attachment_item.file_path.split('\\')[-2])

            response = []
            for file in files:
                file['type_id'] = allowed_file(file['file_extension'], file_types)
                file['user_id'] = user_id
                file['project_id'] = project_id
                file['text'] = ''
                file['user_ids'] = user_ids
                attachment = db_helper.add_item(MODEL, file)
                response.append(attachment)

            return response, 201

        except Exception as e:
            session.rollback()
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error when adding images")
