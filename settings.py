import os,sys

dev_mode = 'win_dev'

#MODULE WITH "CONSTANTS" DO NOT CHANGE ANYTHING
ROOT_DIR =os.path.dirname(os.path.realpath(sys.argv[0]))


def get_upload_folder():
    try:
        if (dev_mode=='win_dev'):
            return 'd:\\Projects\\Backups\\Landau.X\\data\\uploads'
        elif (dev_mode=='prod'):
            return '/home/landau/uploads'
        pass
    except Exception as e:
        return ''

def get_attachments_folder():
    try:
        if (dev_mode=='win_dev'):
            return  'd:\\Projects\\Backups\\Landau.X\\data\\attachments'
        elif (dev_mode=='prod'):
            return '/home/landau/attachments'
        pass
    except Exception as e:
        return ''

def get_env_path():
    try:
        if (dev_mode=='win_dev'):
            return  'd:\\Projects\\Landau.Pyzzle.Engine\\venv\\Scripts\\python.exe'
        elif (dev_mode=='prod'):
            return '/var/www/Landau.Pyzzle.Engine/venv/bin/python'
        pass
    except Exception as e:
        return ''

def get_engine_path():
    try:
        if (dev_mode=='win_dev'):
            return  " d:\Projects\Landau.Pyzzle.Engine\__init__.py "
        elif (dev_mode=='prod'):
            return ' /var/www/Landau.Pyzzle.Engine/__init__.py '
        pass
    except Exception as e:
        return ''

def get_exports_folder():
    try:
        if (dev_mode=='win_dev'):
            return  "d:\\Projects\\Backups\\Landau.X\\data\\exports"
        elif (dev_mode=='prod'):
            return '/home/landau/exports'
        pass
    except Exception as e:
        return ''

def get_export_xlsx_folder():
    try:
        if (dev_mode=='win_dev'):
            return "d:\\Projects\\Backups\\Landau.X\\data\\export_xlsx"

        elif (dev_mode=='prod'):
            return '/home/landau/export_xlsx'
        pass
    except Exception as e:
        return ''

def get_console_static_documents_folder():
    try:
        if (dev_mode=='win_dev'):
            return  "d:\\Projects\\Backups\\Landau.X\\data\\console_static_documents"

        elif (dev_mode=='prod'):
            return '/home/landau/console_static_documents'
        pass
    except Exception as e:
        return ''

def get_temp_folder():
    try:
        if (dev_mode=='win_dev'):
            return  "d:\\Projects\\Backups\\Landau.X\\data\\temp_folder"

        elif (dev_mode=='prod'):
            return '/home/landau/temp_folder'
        pass
    except Exception as e:
        return ''

print("ROOT ="+ROOT_DIR)
#connection string
DB_URI = 'postgresql://postgres:12345678@localhost/landau'

#upload folder
UPLOAD_FOLDER =get_upload_folder()
#attachments folder
ATTACHMENTS_FOLDER =get_attachments_folder()

#allowed extensions
ALLOWED_EXTENSIONS = set(['xls','xlsx'])

ENV_PATH = get_env_path()
#engine path
ENGINE_PATH =ENV_PATH+get_engine_path()

EXPORT_FOLDER = get_exports_folder()

#EXPORT EXCELS
EXPORT_XLSX = get_export_xlsx_folder()

#console static documents
CONSOLE_STATIC_DOCUMENTS =get_console_static_documents_folder()


TEMP_FOLDER ="d:\\Projects\\Backups\\Landau.X\\data\\temp_folder"

SOCKET_URL = 'localhost'