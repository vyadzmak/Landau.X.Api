import os,sys

#MODULE WITH "CONSTANTS" DO NOT CHANGE ANYTHING
ROOT_DIR =os.path.dirname(os.path.realpath(sys.argv[0]))

print("ROOT ="+ROOT_DIR)
#connection string
DB_URI = 'postgresql://postgres:12345678@localhost/landau'
#upload folder
UPLOAD_FOLDER = 'd:\\uploads'

#allowed extensions
ALLOWED_EXTENSIONS = set(['xls','xlsx'])

#engine path
ENGINE_PATH ="python d:\Projects\Github\Landau.Pyzzle.Engine\__init__.py "

EXPORT_FOLDER = "d:\\exports"