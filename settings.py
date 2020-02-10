import os,sys

#MODULE WITH "CONSTANTS" DO NOT CHANGE ANYTHING
ROOT_DIR =os.path.dirname(os.path.realpath(sys.argv[0]))

print("ROOT ="+ROOT_DIR)
#connection string
DB_URI = 'postgresql://postgres:12345678@localhost/landau'
#upload folder
UPLOAD_FOLDER = 'd:\\Projects\\Backups\\Landau.X\\data\\uploads'
#attachments folder
ATTACHMENTS_FOLDER = 'd:\\attachments'

#allowed extensions
ALLOWED_EXTENSIONS = set(['xls','xlsx'])

ENV_PATH = "d:\\Projects\\Github\\Landau.Pyzzle.Engine\\venv\\Scripts\\python.exe"
#engine path
ENGINE_PATH =ENV_PATH+" d:\Projects\Github\Landau.Pyzzle.Engine\__init__.py "

EXPORT_FOLDER = "d:\\Projects\\Backups\\Landau.X\\data\\exports"

#EXPORT EXCELS
EXPORT_XLSX = "d:\\Projects\\Backups\\Landau.X\\data\\export_xlsx"

#console static documents
CONSOLE_STATIC_DOCUMENTS = "d:\\Projects\\Backups\\Landau.X\\data\\console_static_documents"


TEMP_FOLDER ="d:\\Projects\\Backups\\Landau.X\\data\\temp_folder"

SOCKET_URL = 'localhost'