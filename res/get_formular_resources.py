from db_models.models import Formulars
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from flask import Flask, make_response,send_from_directory,send_file
from modules.original_file_saver import save_original_documents_documents

class GetFormularResource(Resource):
    def get(self, id):
        try:
            formular_data = session.query(Formulars).filter(Formulars.id==id).first()
            if (formular_data==None):
                abort(404,message ='File not found')

            return {'file_path':formular_data.file_path}
        except Exception as e:
            abort(404, message="File not found")

