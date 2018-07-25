from db_models.models import DefaultAnalyticRules, AnalyticRules,Reports, Projects,Documents
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import desc
from flask import Flask, make_response,send_from_directory,send_file
from flask import Response
import  urllib.parse as urllib
import modules.project_exporter as project_exporter
import modules.documents_exporter as documents_exporter
class ExportDefaultAnalyticRulesResource(Resource):

    def get(self):
        schema = session.query(DefaultAnalyticRules).first()
        content = schema.data
        response = make_response(content)
        cd = 'attachment; filename=default_schema.json'
        response.headers['Content-Disposition'] = cd
        response.mimetype = 'application/json'
        return response


class ExportAnalyticRulesResource(Resource):

    def get(self,id):
        schema = session.query(AnalyticRules).filter(AnalyticRules.id==id).first()
        content = schema.data
        response = make_response(content)
        name ="Схема ("+schema.name+")"+".json"
        t =name.encode('utf-8')
        name = t.decode("utf-8")
        name = urllib.quote(name)
        cd = 'attachment; filename='+name
        response.headers['Content-Disposition'] = cd
        response.mimetype = 'application/json'
        return response

class ExportProjectsResource(Resource):

    def get(self,id):
        try:
            report = session.query(Reports).filter(Reports.project_id==id).first()
            project =session.query(Projects).filter(Projects.id==id).first()
            if not report:
                abort(404, message="Report {} doesn't exist".format(id))

            if not project:
                abort(404, message="Project {} doesn't exist".format(id))

            project_name = project.name
            project_folder, export_path = project_exporter.export_project(project_name,report.data)
            #return {}
            return send_from_directory(project_folder,export_path, as_attachment=True)
            #return send_file(filename_or_fp=export_path,as_attachment=True)
        except Exception as e:
            return {}

class ExportDocumentsResource(Resource):

    def get(self,id):
        try:
            documents = session.query(Documents).filter(Documents.project_id==id).all()

            if not documents:
                abort(404, message="Documents {} doesn't exist".format(id))


            export_folder, export_path = documents_exporter.export_documents(documents)
            return send_from_directory(export_folder,export_path, as_attachment=True)
        except Exception as e:
            return {}


class ExportSingleDocumentResource(Resource):
    def get(self, id):
        try:
            document = session.query(Documents).filter(Documents.id == id).first()

            if not document:
                abort(404, message="Document {} doesn't exist".format(id))


            export_folder, export_path = documents_exporter.export_single_document(document)
            return send_from_directory(export_folder, export_path, as_attachment=True)
        except Exception as e:
            return {}