from db_models.models import ProjectAttachmentTypes
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort,reqparse

attachment_type_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'system_name': fields.String,
    'filename_extensions': fields.List(fields.String),
    'icon': fields.String
}

parser = reqparse.RequestParser()

class ProjectAttachmentTypeResource(Resource):
    @marshal_with(attachment_type_fields)
    def get(self, id):
        try:
            attachment_type = session.query(ProjectAttachmentTypes).filter(ProjectAttachmentTypes.id == id).first()
            if not attachment_type:
                abort(404, message="Attachment type {} doesn't exist".format(id))
            return attachment_type
        except Exception as e:
            session.rollback()
            abort(400, message="Error while getting record Attachment Type")

    def delete(self, id):
        try:
            attachment_type = session.query(ProjectAttachmentTypes).filter(ProjectAttachmentTypes.id == id).first()
            if not attachment_type:
                abort(404, message="Attachment type {} doesn't exist".format(id))
            session.delete(attachment_type)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while deleting record Attachment Type")

    @marshal_with(attachment_type_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            attachment_type = session.query(ProjectAttachmentTypes).filter(ProjectAttachmentTypes.id == id).first()
            attachment_type.name = json_data['name']
            attachment_type.system_name = json_data['system_name']
            attachment_type.filename_extensions = json_data['filename_extensions']
            attachment_type.icon = json_data['icon']
            session.add(attachment_type)
            session.commit()
            return attachment_type, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while updating record Attachment Type")

class ProjectAttachmentTypeListResource(Resource):
    @marshal_with(attachment_type_fields)
    def get(self):
        try:
            attachment_types = session.query(ProjectAttachmentTypes).all()
            return attachment_types
        except Exception as e:
            session.rollback()
            abort(400, message="Error while getting records Attachment Type")

    @marshal_with(attachment_type_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            attachment_type = ProjectAttachmentTypes(json_data["name"],json_data["system_name"],
                                                     json_data["filename_extensions"],json_data["icon"])
            session.add(attachment_type)
            session.commit()
            return attachment_type, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Attachment Type")