from db_models.models import DefaultAnalyticRules, AnalyticRules,Reports, Projects,Documents,ProjectAttachments,ReportHistory
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from flask import Flask, make_response,send_from_directory,send_file
from modules.original_file_saver import save_original_documents_documents

class ExportExcludeTransactionsDocumentsResource(Resource):
    def get(self, id):
        try:

            folder_path,zip_file_name,output_file_name = save_original_documents_documents(id)
            if (folder_path==None or zip_file_name==None or output_file_name==None):
                return make_response('Files not found',400)

            return send_from_directory(folder_path, zip_file_name, attachment_filename=output_file_name, as_attachment=True)
        except Exception as e:
            abort(404, message="File not found")

