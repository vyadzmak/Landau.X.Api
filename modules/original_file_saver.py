import os
import re
import uuid
from pathlib import Path
from db_models.models import Projects, Documents
from settings import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, ATTACHMENTS_FOLDER, EXPORT_FOLDER
import string
from transliterate import translit, get_available_language_codes

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
import shutil
from db.db import session
from sqlalchemy import and_


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# save original documents
def save_original_documents_documents(project_id):
    try:

        documents = session.query(Documents).filter(
            and_(Documents.project_id == project_id, Documents.file_path != '')).all()

        if (documents == None):
            return None, None, None

        file_path = documents[0].file_path

        files_exists = False
        for document in documents:
            e = os.path.isfile(document.file_path)
            if (e==True):
                files_exists =True
                break

        if (files_exists==False):
            return None,None,None

        p = Path(file_path)

        source_dir = p.parent
        project = session.query(Projects).filter(Projects.id == project_id).first()
        project_name = ''
        if (project != None):
            project_name = project.name
            project_name = str(project_name).replace('"', ' ')
            project_name = translit(project_name, 'ru', reversed=True)

            if (project_name == ''):
                project_name = 'export_project_' + str(project_id)
        project_name = str(project_name).replace(' ','_')
        arch_name = os.path.join(EXPORT_FOLDER, project_name)
        try:
            shutil.make_archive(arch_name, 'zip', source_dir)

            return EXPORT_FOLDER, project_name + '.zip', project_name + '.zip'
        except Exception as e:
            return None, None, None

    except Exception as e:
        print(str(e))
        pass
