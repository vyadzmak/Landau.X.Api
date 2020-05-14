from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from flask import Flask, request
from modules.file_saver import save_formular_documents
from modules.log_helper_module import add_log
from db_models.models import FormularVersionStorage,ClientProducts
class FormularVersionsStorageResources(Resource):

    def post(self):
        try:

            f = request.form
            user_id = int(f.get('user_id'))
            project_id = int(f.get('project_id'))
            files = save_formular_documents(request.files, project_id)
            #     # adding file_data to db
            for file_data in files:
                formular = FormularVersionStorage(project_id,user_id,file_data['file_path'])
                session.add(formular)
                session.commit()
            return {"State": "OK"}
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            return {"State": "Error"}
