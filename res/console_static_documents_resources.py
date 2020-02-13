from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from flask import Flask, request,make_response
from modules.file_saver import save_console_static_documents
from modules.log_helper_module import add_log
from db_models.models import FormularVersionStorage,ClientProducts
from modules.console_static_documents_processor import process_documents
from modules.json_serializator import encode_json
from db_models.models import ConsolidateStaticDocuments
class ConsoleStaticDocumentsResources(Resource):

    def post(self):
        try:


            f = request.form
            user_id = int(f.get('user_id'))
            name = str(f.get('name'))
            files = save_console_static_documents(request.files, name)
            result = process_documents(files)
            if (result.has_error==True):
                return make_response('Documents has errors',400)

            else:
                data = encode_json(result)
                model = ConsolidateStaticDocuments(user_id,name,data,'')

                session.add(model)
                session.commit()

                file_names = []

                if (result.balance_static_document!=None):
                    file_names.append(result.balance_static_document.file_name)

                if (result.opiu_static_document != None):
                    file_names.append(result.opiu_static_document.file_name)

                if (result.deb_credit_certificate != None):
                    file_names.append(result.deb_credit_certificate.file_name)

                result = {
                    'id':model.id,
                    'name': name,
                    'file_names':file_names
                }
                return result


        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            return {"State": "Error"}


    def put(self, id):

        json_data = request.get_json(force=True)
        project_id = json_data['project_id']
        console_static_document = session.query(ConsolidateStaticDocuments).filter(ConsolidateStaticDocuments.id==id).first()
        if (not console_static_document):
            abort(404, error='Consolidate static not found')
        console_static_document.project_id = project_id
        session.add(console_static_document)
        session.commit()
        return  201