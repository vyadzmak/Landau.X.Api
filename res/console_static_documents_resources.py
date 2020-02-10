from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from flask import Flask, request
from modules.file_saver import save_console_static_documents
from modules.log_helper_module import add_log
from db_models.models import FormularVersionStorage,ClientProducts
from modules.console_static_documents_processor import process_documents

class ConsoleStaticDocumentsResources(Resource):

    def post(self):
        try:


            f = request.form
            user_id = int(f.get('user_id'))
            project_id = int(f.get('project_id'))
            name = str(f.get('name'))
            files = save_console_static_documents(request.files, name)
            result = process_documents(files)
            return {"State": "OK"}
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            return {"State": "Error"}
