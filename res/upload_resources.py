from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import os
import werkzeug
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from db_models.models import Projects,Documents
import uuid
UPLOAD_FOLDER = 'd:\\uploads'
ALLOWED_EXTENSIONS = set(['xls','xlsx'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



class UploadFile(Resource):
    def post(self):
        try:
            f = request.form
            userId = f.get('userId')
            project = Projects(userId)
            session.add(project)
            session.commit()
            if (project.id>-1):
                files= request.files.getlist("")
                for file in files:
                    print(file.filename)
                    if file and allowed_file(file.filename):
                        # From flask uploading tutorial
                        filename =str(secure_filename(file.filename)).lower()
                        sec_name =(str(uuid.uuid1()))+'.'+filename
                        file_path = os.path.join(UPLOAD_FOLDER,sec_name)
                        file.save(file_path)
                        file_size = os.path.getsize(file_path)
                        document = Documents(project.id,userId,file.filename,file_path,file_size)
                        session.add(document)
                        session.commit()

                        #return {}
                    else:
                        # return error
                        return {}
                return {"State":"OK"}
        except Exception as e:
            return {"State":"Error"}
