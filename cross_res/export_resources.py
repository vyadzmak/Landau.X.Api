from db_models.modelsv2 import DefaultAnalyticRules, AnalyticRules, Reports, Projects, Documents, ProjectAttachments
from db.db import session
from flask_restful import Resource, abort
from flask import Flask, make_response, send_from_directory
import urllib.parse as urllib
import modules.project_exporter as project_exporter
import modules.documents_exporter as documents_exporter
from modules.log_helper_module import add_log
from sqlalchemy import and_


class ExportDefaultAnalyticRulesResource(Resource):
    def __init__(self):
        self.route = "/v2/exportDefaultSchema"
        self.end_point = "v2-export-default-schema"

    def get(self):
        try:
            schema = session.query(DefaultAnalyticRules).first()
            content = schema.data
            response = make_response(content)
            cd = 'attachment; filename=default_schema.json'
            response.headers['Content-Disposition'] = cd
            response.mimetype = 'application/json'
            return response
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, "Export Default Analytic Rules error")


class ExportAnalyticRulesResource(Resource):
    def __init__(self):
        self.route = "/v2/exportSchema/<int:id>"
        self.end_point = "v2-export-schema"

    def get(self, id):
        try:
            schema = session.query(AnalyticRules).filter(AnalyticRules.id == id).first()
            content = schema.data
            response = make_response(content)
            name = "Схема (" + schema.name + ")" + ".json"
            t = name.encode('utf-8')
            name = t.decode("utf-8")
            name = urllib.quote(name)
            cd = 'attachment; filename=' + name
            response.headers['Content-Disposition'] = cd
            response.mimetype = 'application/json'
            return response
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, "Export Analytic Rules error")

class ExportProjectsResource(Resource):
    def __init__(self):
        self.route = "/v2/exportProject/<int:id>"
        self.end_point = "v2-export-project"

    def get(self, id):
        try:
            report = session.query(Reports).filter(Reports.project_id == id).first()
            project = session.query(Projects).filter(Projects.id == id).first()
            if not report:
                abort(404, message="Report {} doesn't exist".format(id))

            if not project:
                abort(404, message="Project {} doesn't exist".format(id))

            project_name = project.name
            project_folder, export_path = project_exporter.export_project(project_name, report.data)
            # return {}
            return send_from_directory(project_folder, export_path, as_attachment=True)
            # return send_file(filename_or_fp=export_path,as_attachment=True)
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, "Export Project error")


class ExportDocumentsResource(Resource):
    def __init__(self):
        self.route = "/v2/exportDocuments/<int:id>"
        self.end_point = "v2-export-document"

    def get(self, id):
        try:
            documents = session.query(Documents).filter(
                and_(Documents.project_id == id, Documents.document_state_id == 3)).all()

            if not documents:
                abort(404, message="Documents {} doesn't exist".format(id))

            export_folder, export_path = documents_exporter.export_documents(documents)
            return send_from_directory(export_folder, export_path, as_attachment=True)
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, "Export Documents error")


class ExportSingleDocumentResource(Resource):
    def __init__(self):
        self.route = "/v2/exportSingleDocument/<int:id>"
        self.end_point = "v2-export-single-document"

    def get(self, id):
        try:
            document = session.query(Documents).filter(Documents.id == id).first()

            if not document:
                abort(404, message="Document {} doesn't exist".format(id))

            export_folder, export_path = documents_exporter.export_single_document(document)
            return send_from_directory(export_folder, export_path, as_attachment=True)
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, "Export Single Document error")


class ExportProjectAttachmentResource(Resource):
    def __init__(self):
        self.route = "/v2/exportProjectAttachment/<int:id>"
        self.end_point = "v2-export-project-attachment"

    def get(self, id):
        try:
            attachment = session.query(ProjectAttachments).filter(ProjectAttachments.id == id).first()
            actual_file_name = attachment.file_path.split('\\')[-1]
            folder_path = "\\".join(attachment.file_path.split('\\')[:-1])
            t = attachment.file_name.encode('utf-8')
            original_file_name = t.decode("utf-8")
            original_file_name = urllib.quote(original_file_name)
            return send_from_directory(folder_path, actual_file_name, attachment_filename=original_file_name,
                                       as_attachment=True)
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, "Export Project Attachment error")
