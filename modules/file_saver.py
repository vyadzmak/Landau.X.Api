import os
import re
import uuid
from pathlib import Path

from settings import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, ATTACHMENTS_FOLDER, EXPORT_XLSX
import datetime

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_documents(request_files, dir_id=str(uuid.uuid4().hex)):
    documents = []
    project_folder = os.path.join(UPLOAD_FOLDER, dir_id)
    for file in request_files.values():
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)
        if file and allowed_file(file.filename):
            # From flask uploading tutorial
            filename = file.filename  # str(secure_filename(file.filename)).lower()
            short_name = Path(filename).stem

            short_name = re.sub(r'[\\/*?:"<>|]', "", short_name)

            extension = Path(filename).suffix
            file_id = str(uuid.uuid4().hex)
            result_file_name = short_name + "_" + file_id + extension

            l_res_file_name = len(result_file_name)
            l_project_folder = len(project_folder)

            if l_res_file_name + l_project_folder > 250:
                result_file_name = file_id + extension

            print("Save to " + result_file_name)
            file_path = os.path.join(project_folder, result_file_name)
            file.save(file_path)
            file_size = os.path.getsize(file_path)
            documents.append({
                'file_name': filename,
                'file_path': file_path,
                'file_size': file_size
            })

    return documents

    # generate export file name
def generate_export_file_name():
        try:
            d = datetime.datetime.now()

            d = re.sub("\D", "", str(d))

            #clear_project_name = str(project_name).replace(' ', '_')
            #clear_project_name = re.sub(r'[\W_]+', '_', clear_project_name)
            file_name = 'F_V_' + str(d) + '.xlsx'

            full_path_xlsx = file_name

            full_path_xlsx = str(full_path_xlsx).replace('___', '_')
            full_path_xlsx = str(full_path_xlsx).replace('__', '_')

            return full_path_xlsx
        except Exception as e:
            pass

def save_formular_documents(request_files, dir_id):
    documents = []
    project_folder = os.path.join(EXPORT_XLSX, str(dir_id))
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    for file in request_files.values():
        # From flask uploading tutorial
        filename = file.filename  # str(secure_filename(file.filename)).lower()
        short_name = Path(filename).stem
        result_file_name = generate_export_file_name()

        print("Save to " + result_file_name)
        file_path = os.path.join(project_folder, result_file_name)
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        documents.append({
            'file_name': filename,
            'file_path': file_path,
            'file_size': file_size
        })


    return documents


def save_attachments(request_files, dir_id=str(uuid.uuid4().hex)):
    result = []
    upload_folder = os.path.join(ATTACHMENTS_FOLDER, dir_id)
    for file in request_files.values():
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        if file:
            # From flask uploading tutorial
            filename = file.filename  # str(secure_filename(file.filename)).lower()

            extension = Path(filename).suffix
            file_id = str(uuid.uuid4().hex)
            result_file_name = file_id + extension

            l_res_file_name = len(result_file_name)
            l_upload_folder = len(upload_folder)

            if l_res_file_name + l_upload_folder > 250:
                result_file_name = file_id + extension

            print("Save to " + result_file_name)
            file_path = os.path.join(upload_folder, result_file_name)
            file.save(file_path)
            file_size = os.path.getsize(file_path)
            result.append({
                'file_name': filename,
                'file_path': file_path,
                'file_size': file_size,
                'file_extension': extension
            })

    return result
