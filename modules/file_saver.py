import os
import re
import uuid
from pathlib import Path

from settings import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, ATTACHMENTS_FOLDER


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
