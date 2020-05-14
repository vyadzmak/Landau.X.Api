import os
import re
import subprocess
import unicodedata
import uuid
from pathlib import Path

from flask import request
from flask_restful import Resource

from db.db import session
from db_models.models import Documents,Formulars,Users
from settings import ENGINE_PATH, ATTACHMENTS_FOLDER, ALLOWED_EXTENSIONS


# UPLOAD_FOLDER = 'd:\\uploads'
# ALLOWED_EXTENSIONS = set(['xls','xlsx'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_file_name():
    pass


class UploadFormular(Resource):
    def post(self):
        try:
            f = request.form
            user_id = f.get('user_id')

            user = session.query(Users).filter(Users.id==user_id).first()
            client_id = user.client_id
            session.commit()
            f_list = []
            files = []
            for t in request.files:
                f_list = request.files.getlist(str(t))
                for j_file in f_list:
                    files.append(j_file)
            project_folder = ATTACHMENTS_FOLDER
            result = []
            for file in files:

                if not os.path.exists(project_folder):
                    os.makedirs(project_folder)
                if file and allowed_file(file.filename):
                    # From flask uploading tutorial
                    filename = file.filename
                    filename = unicodedata.normalize('NFC', filename).encode('utf-8').decode('utf-8')
                    v = Path(filename)
                    short_name = Path(filename).stem

                    short_name = re.sub(r'[\\/*?:"<>|]', "", short_name)

                    extension = Path(filename).suffix
                    file_id = str(uuid.uuid4().hex)
                    result_file_name = short_name + "_" + file_id + extension

                    l_res_file_name = len(result_file_name)
                    l_project_folder = len(project_folder)

                    if (l_res_file_name + l_project_folder > 250):
                        result_file_name = file_id + extension

                    print("Save to " + result_file_name)
                    file_path = os.path.join(project_folder, result_file_name)
                    file.save(file_path)
                    file_size = os.path.getsize(file_path)
                    formular = Formulars(client_id,user_id,file.filename,file_path,file_size)
                    session.add(formular)
                    session.commit()
                    item = {
                        'id':formular.id,
                        'file_name':file.filename,
                        'creation_date':str(formular.creation_date)
                    }
                    result.append(item)
                    # return {}
                else:
                    # return error
                    return {}
            return result
        except Exception as e:
            session.rollback()
            return {"State": "Error"}
