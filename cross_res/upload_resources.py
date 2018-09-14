from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from flask import Flask, request
from db_models.modelsv2 import Projects, Documents

from modules.engine_module import add_job
from modules.file_saver import save_documents
from modules.db_helper import add_item as add_to_db
from modules.log_helper_module import add_log

#PARAMS
ENTITY_NAME = "Project Upload"
MODEL = Projects
ROUTE ="/v2/upload"
END_POINT = "v2-project-upload"

class UploadProject(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass


    def post(self):
        try:
            f = request.form
            userId = f.get('userId')
            project = add_to_db(Projects, {"user_id": userId})
            if project.id > -1:
                # saving files to filesystem
                files = save_documents(request.files)
                # adding file_data to db
                for file_data in files:
                    file_data['project_id'] = project.id
                    file_data['user_id'] = userId
                    add_to_db(Documents, file_data)
                # adding job for engine and starting it
                add_job(project.id, userId, " 0 -1")
                return {"State": "OK"}
            return {"State": "Error"}
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            return {"State": "Error"}
