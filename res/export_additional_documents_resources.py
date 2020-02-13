from db_models.models import ConsolidateStaticDocuments, ConsolidateExcludeTransactionsDocuments
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from flask import Flask, make_response, send_from_directory, send_file, request
from modules.original_file_saver import save_original_documents_documents
from pathlib import Path
import pandas as pd
import numpy as np
import json
from modules.documents_exporter import translit,clean_filename
from settings import EXPORT_FOLDER
import os
import uuid
class ExportExcludeTransactionsDocumentsResource(Resource):
    def get(self, id):
        try:
            document = session.query(ConsolidateExcludeTransactionsDocuments).filter(
                ConsolidateExcludeTransactionsDocuments.id == id).first()

            if (not document):
                return make_response('Files not found', 400)
            data = json.loads(document.data)
            balance_header = data['balance_header']
            balance_data = data['balance_data']
            if (len(balance_data) > 0):
                balance_frame = pd.DataFrame(np.array(balance_data),
                                             columns=balance_header)
            else:
                balance_frame = pd.DataFrame(
                    columns=balance_header)
            balance_frame.drop(columns=['', 'id'], inplace=True)

            opiu_header = data['opiu_header']
            opiu_data = data['opiu_data']
            if (len(opiu_data) > 0):
                opiu_frame = pd.DataFrame(np.array(opiu_data),
                                          columns=opiu_header)
            else:
                opiu_frame = pd.DataFrame(columns=opiu_header)

            opiu_frame.drop(columns=['', 'id'], inplace=True)

            odds_header = data['odds_header']
            odds_data = data['odds_data']
            if (len(odds_data) > 0):
                odds_frame = pd.DataFrame(np.array(odds_data),
                                          columns=odds_header)
            else:
                odds_frame = pd.DataFrame(
                    columns=odds_header)

            odds_frame.drop(columns=['', 'id'], inplace=True)

            dir_id = str(uuid.uuid4().hex)
            project_folder = os.path.join(EXPORT_FOLDER, dir_id)
            if not os.path.exists(project_folder):
                os.makedirs(project_folder)
            name = 'export_exclude_data_'+document.name+'.xls'

            name = str(name).replace('"', ' ')
            name = translit(name, 'ru', reversed=True)

            file_name = clean_filename(name)
            file_name = file_name.replace('__', "_")




            export_path = os.path.join(project_folder,name)

            with pd.ExcelWriter(export_path) as writer:
                balance_frame.to_excel(writer, sheet_name='Баланс')
                opiu_frame.to_excel(writer, sheet_name='ОПиУ')

                odds_frame.to_excel(writer, sheet_name='ОДДС')

            return send_from_directory(project_folder, file_name,
                                       as_attachment=True)

        except Exception as e:
            abort(404, message="File not found")


class ExportStaticDocumentsResource(Resource):
    def post(self):
        try:

            json_data = request.get_json(force=True)
            project_id = json_data["project_id"]
            document_id = json_data["document_id"]

            static_document = session.query(ConsolidateStaticDocuments).filter(
                ConsolidateStaticDocuments.project_id == project_id).order_by(
                ConsolidateStaticDocuments.id.desc()).first()

            balance_static_document_id = static_document.data['balance_static_document']['id']
            opiu_static_document_id = static_document.data['opiu_static_document']['id']
            deb_credit_certificate_id = static_document.data['deb_credit_certificate']['id']

            file_path = ''

            if (balance_static_document_id == document_id):
                file_path = static_document.data['balance_static_document']['file_path']
            elif (opiu_static_document_id == document_id):
                file_path = static_document.data['opiu_static_document']['file_path']
            elif (deb_credit_certificate_id == document_id):
                file_path = static_document.data['deb_credit_certificate']['file_path']

            if (file_path == ''):
                return make_response('Files not found', 400)

            p = Path(file_path)

            folder_path = p.parent
            file_path = p.stem
            file_ext = p.suffix
            name = str(file_path + file_ext).replace(' ', '_')



            name = str(name).replace('"', ' ')
            name = translit(name, 'ru', reversed=True)

            file_name = clean_filename(name)
            file_name = file_name.replace('__', "_")


            return send_from_directory(folder_path, file_path + file_ext, attachment_filename=file_name,
                                       as_attachment=True)
        except Exception as e:
            abort(404, message="File not found")
