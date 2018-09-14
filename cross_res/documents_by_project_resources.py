from db_models.modelsv2 import Documents, Projects
from resv2.documents_resources import OUTPUT_FIELDS as DOCUMENT_FIELDS
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from modules.json_serializator import engine_encode
import modules.db_helper as db_helper
from modules.str_bytes_converter import to_str
from modules.log_helper_module import add_log
from modules.file_saver import save_documents
import json

project_state_fields = {
    'id': fields.Integer,
    'name': fields.String
}

project_fields = {
    'id': fields.Integer,
    'state_id': fields.Integer,
    'project_state': fields.Nested(project_state_fields)
}

OUTPUT_FIELDS = {
    'project': fields.Nested(project_fields),
    'documents': fields.List(fields.Nested(DOCUMENT_FIELDS))
}


class ProjectDocumentListResource(Resource):
    def __init__(self):
        self.route = "/v2/projectDocuments/<int:id>"
        self.end_point = "v2-project-documents-list"

    @marshal_with(DOCUMENT_FIELDS)
    def get(self, id):
        try:
            documents = session.query(Documents).filter(Documents.project_id == id).all()
            if not documents:
                abort(404, message="Documents not found")
            return documents
        except Exception as e:
            session.rollback()
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting documents")


class BatchDocumentListResource(Resource):
    def __init__(self):
        self.route = "/v2/batchDocuments"
        self.end_point = "v2-batch-documents-list"

    @marshal_with(DOCUMENT_FIELDS)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            items = json.loads(json_data)

            for item in items:
                _id = int(item["id"])
                if (_id != -1):
                    item["data"] = engine_encode(item["data"])
                    update_item = {k: item[k] for k in ["document_state_id", "document_type_id", "data"] if k in item}
                    db_helper.update_item(Documents, update_item, _id)
                else:
                    db_helper.update_item(Documents, update_item, _id)
                    item["data"] = engine_encode(item["data"])
                    add_item = {k: item[k] for k in
                                ["project_id", "user_id", "file_name", "file_path",
                                 "file_size", "document_state_id", "document_type_id", "data"]
                                if k in item}
                    db_helper.add_item(Documents, add_item)
                    pass
            return {}, 201
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while adding record Document")


class ExcludeDocumentListResource(Resource):
    def __init__(self):
        self.route = "/v2/excludeDocuments"
        self.end_point = "v2-exclude-documents-list"

    @marshal_with(OUTPUT_FIELDS)
    def post(self):
        try:
            json_data = request.get_json(force=True)

            project = db_helper.update_item(Projects, {'state_id': 6}, json_data["project_id"])
            if project is None:
                abort(404, message="Include-exclude document operation. Project not found")

            documents = session.query(Documents).filter(Documents.id.in_(json_data["document_ids"])).all()
            for document in documents:
                document.is_excluded = not document.is_excluded
                session.add(document)
                session.commit()
            return {'project': project, 'documents': documents}, 201
        except Exception as e:
            session.rollback()
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while include-exclude Document")


class UploadAdditionalFile(Resource):
    def __init__(self):
        self.route = "/v2/uploadAdditional"
        self.end_point = "v2-upload-additional-file"

    @marshal_with(OUTPUT_FIELDS)
    def post(self):
        try:
            f = request.form
            user_id = f.get('userId')
            project_id = f.get('projectId')

            project = db_helper.update_item(Projects, {'state_id': 6}, project_id)
            if project is None:
                abort(404, message="Project not found")
            documents = []

            document = session.query(Documents).filter(
                Documents.project_id == project_id).first()
            # saving files to filesystem
            if document is None:
                files = save_documents(request.files)
            else:
                files = save_documents(request.files, document.file_path.split('\\')[-2])

            # adding file_data to db
            for file_data in files:
                file_data['project_id'] = project.id
                file_data['user_id'] = user_id
                db_helper.add_item(Documents, file_data)

            return {'project': project, 'documents': documents}, 201

        except Exception as e:
            session.rollback()
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while include-exclude Document")
