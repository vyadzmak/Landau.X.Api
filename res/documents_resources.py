from db_models.models import Documents
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
import copy
import zlib
import base64

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode() # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value # Instance of bytes


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode() # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value
user_role_fields = {
    'name': fields.String,
    'id': fields.Integer
}

client_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name"),
    'registration_date': fields.DateTime(attribute="registration_date"),
    'registration_number': fields.String(attribute="registration_number")
}
user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'client_id': fields.Integer,
    'lock_state': fields.Boolean,
    'user_role_id': fields.Integer,
    'user_role': fields.Nested(user_role_fields),
    'client': fields.Nested(client_fields)

}
document_state_fields = {
    'id': fields.Integer,
    'name': fields.String
}

document_fields = {
    'id': fields.Integer,
    'file_name': fields.String,
    'file_path': fields.String,
    'file_size': fields.Float,
    'created_date': fields.DateTime,
    'document_state_id': fields.Integer,
    'document_state': fields.Nested(document_state_fields),
    'user_id': fields.Integer,
    'user_data': fields.Nested(user_fields),


}

f_document_fields = {
    'id': fields.Integer,
    'file_name': fields.String,
    'file_path': fields.String,
    'file_size': fields.Float,
    'created_date': fields.DateTime,
    'document_state_id': fields.Integer,
    #'document_state': fields.Nested(document_state_fields),
    'user_id': fields.Integer,
    #'user_data': fields.Nested(user_fields),
    'data': fields.String

}

class ProjectDocumentListResource(Resource):
    @marshal_with(document_fields)
    def get(self, id):
        documents = session.query(Documents).filter(Documents.project_id == id).all()
        if not documents:
            abort(404, message="Documents not found")
        return documents

import jsonpickle
def encode(ob):
    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False);
        #jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        json_s = jsonpickle.encode(ob, unpicklable=True)
        return json_s
    except Exception as e:
        print(str(e))
        return ""


class BatchDocumentListResource(Resource):
    @marshal_with(document_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            items = json.loads(json_data)

            for item in items:
                _id = int(item["id"])
                document = session.query(Documents).filter(Documents.id == _id).first()
                document.document_state_id = item["document_state_id"]
                document.document_type_id = item["document_type_id"]
                document.data = encode(item["data"])
                session.add(document)
                session.commit()
            return {}, 201
        except Exception as e:
            abort(400, message="Error while adding record Document")
class DocumentResource(Resource):
    @marshal_with(f_document_fields)
    def get(self, id):
        document ={}

        document = session.query(Documents).filter(Documents.id == id).first()
        if not document:
            abort(404, message="Document {} doesn't exist".format(id))
        result_document = copy.deepcopy(document)

        s_cmpstr = result_document.data
        s_cmpstr = s_cmpstr.replace("b'", "")
        s_cmpstr = s_cmpstr.replace("'", "")
        b_cmpstr = to_bytes(s_cmpstr)
        b_cmpstr = base64.b64decode(b_cmpstr)
        dec = zlib.decompress(b_cmpstr)
        rr = to_str(dec)
        #result_document.document_state = document.document_state
        result_document.data =  rr



        return result_document

    def delete(self, id):
        document = session.query(Documents).filter(Documents.id == id).first()
        if not document:
            abort(404, message="Document {} doesn't exist".format(id))
        session.delete(document)
        session.commit()
        return {}, 204

    @marshal_with(document_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        json_data = json.loads(json_data)
        document = session.query(Documents).filter(Documents.id == id).first()
        document.document_state_id = json_data["document_state_id"]
        document.document_type_id = json_data["document_type_id"]
        document.data = encode(json_data["data"])
        session.add(document)
        session.commit()
        return document, 201


class DocumentListResource(Resource):
    @marshal_with(document_fields)
    def get(self):
        documents = session.query(Documents).all()
        return documents

    @marshal_with(document_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            # file_name,file_path,file_size
            document = Documents(projectId=json_data["projectId"],
                                 userId=json_data["user_id"], file_name=json_data["file_name"],
                                 file_path=json_data["file_path"], file_size=json_data["file_size"])
            session.add(document)
            session.commit()
            return document, 201
        except Exception as e:
            abort(400, message="Error while adding record Document")
