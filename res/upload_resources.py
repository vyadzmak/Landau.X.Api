from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import os
import werkzeug
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from db_models.models import Projects,Documents,Chats
import uuid
import re
import subprocess
from pathlib import Path
from settings import ENGINE_PATH, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import unicodedata

#UPLOAD_FOLDER = 'd:\\uploads'
#ALLOWED_EXTENSIONS = set(['xls','xlsx'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_file_name():
    pass
class UploadFile(Resource):
    def post(self):
        try:
            f = request.form
            userId = f.get('userId')
            project = Projects(userId)
            session.add(project)
            session.commit()
            system_chat = Chats('Обсуждение проекта', userId, project.id, [], True)
            session.add(system_chat)
            session.commit()
            if (project.id>-1):
                f_list =[]
                files =[]
                for t in request.files:
                    f_list = request.files.getlist(str(t))
                    for j_file in f_list:
                        files.append(j_file)
                #files= request.files.getlist("file[]")
                dir_id = str(uuid.uuid4().hex)
                project_folder = os.path.join(UPLOAD_FOLDER, dir_id)
                for file in files:


                    if not os.path.exists(project_folder):
                        os.makedirs(project_folder)
                    if file and allowed_file(file.filename):
                        # From flask uploading tutorial
                        filename =file.filename #str(secure_filename(file.filename)).lower()
                        filename = unicodedata.normalize('NFC', filename).encode('utf-8').decode('utf-8')
                        v = Path(filename)
                        short_name = Path(filename).stem


                        short_name = re.sub(r'[\\/*?:"<>|]', "", short_name)

                        extension =  Path(filename).suffix
                        file_id =str(uuid.uuid4().hex)
                        result_file_name = short_name+"_"+file_id+extension

                        l_res_file_name = len(result_file_name)
                        l_project_folder =len(project_folder)

                        if (l_res_file_name+l_project_folder >250):
                            result_file_name = file_id+extension

                        print("Save to "+result_file_name)
                        file_path = os.path.join(project_folder,result_file_name)
                        file.save(file_path)
                        file_size = os.path.getsize(file_path)
                        document = Documents(project.id,userId,file.filename,file_path,file_size)
                        session.add(document)
                        session.commit()

                        #return {}
                    else:
                        # return error
                        return {}

                #"python d:\Projects\Github\Landau.Pyzzle.Engine\__init__.py "

                tt = ENGINE_PATH+str(project.id)+" "+str(userId)+" 0 -1"+' none'
                subprocess.Popen(tt, shell=True)
                return {"State":"OK"}
        except Exception as e:
            session.rollback()
            return {"State":"Error"}


