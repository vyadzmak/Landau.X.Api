from db_models.models import ConsolidateExcludeTransactionsDocuments,ConsolidateStaticDocuments
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
from models.additional_project_documents_models.additional_project_document_models import AdditionalProjectDocuments,ConsolidationStaticDocument,ExcludeTransactionsProjectDocument
from modules.json_serializator import encode

class ProjectAdditionalDocumentsResource(Resource):
    def get(self, id):
        try:

            exclude_transaction_documents = session.query(ConsolidateExcludeTransactionsDocuments).filter(ConsolidateExcludeTransactionsDocuments.project_id==id).all()
            static_document = session.query(ConsolidateStaticDocuments).filter(ConsolidateStaticDocuments.project_id==id).order_by(ConsolidateStaticDocuments.id.desc()).first()

            result = AdditionalProjectDocuments()

            if (exclude_transaction_documents!=None):
                for exclude_transaction_document in exclude_transaction_documents:
                    e_document = ExcludeTransactionsProjectDocument()
                    e_document.id =exclude_transaction_document.id
                    e_document.name = exclude_transaction_document.name

                    result.exclude_transactions_document.append(e_document)

            if (static_document!=None):
                    name = static_document.name

                    balance_static_document = ConsolidationStaticDocument()
                    balance_static_document.id = static_document.data['balance_static_document']['id']
                    balance_static_document.name  =name
                    balance_static_document.file_name=static_document.data['balance_static_document']['file_name']

                    result.additional_consolidate_static_documents.append(balance_static_document)

                    opiu_static_document = ConsolidationStaticDocument()
                    opiu_static_document.id = static_document.data['opiu_static_document']['id']
                    opiu_static_document.name = name
                    opiu_static_document.file_name = static_document.data['opiu_static_document']['file_name']

                    result.additional_consolidate_static_documents.append(opiu_static_document)

                    deb_credit_certificate = ConsolidationStaticDocument()
                    deb_credit_certificate.id = static_document.data['deb_credit_certificate']['id']
                    deb_credit_certificate.name = name
                    deb_credit_certificate.file_name = static_document.data['deb_credit_certificate']['file_name']

                    result.additional_consolidate_static_documents.append(deb_credit_certificate)

                    t=0


            result = encode(result)

            return result

            pass
        except Exception as e:
            print(str(e))
            return None

