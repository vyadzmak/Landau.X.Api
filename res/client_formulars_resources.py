from flask import request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

from db.db import session
from db_models.models import Formulars

formular_fields = {
    'id': fields.Integer,
    'file_name': fields.String,
    'creation_date':fields.DateTime
}

parser = reqparse.RequestParser()

class ClientFormularsResource(Resource):
    def delete(self, id):
        try:
            formular = session.query(Formulars).filter(Formulars.id == id).first()
            if not formular:
                abort(404, message="Formular {} doesn't exist".format(id))
            session.delete(formular)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while deleting record Formular")

class ClientFormularListResource(Resource):
    @marshal_with(formular_fields)
    def get(self,id):
        try:
            formulars = session.query(Formulars).filter(Formulars.client_id==id).all()
            return formulars
        except Exception as e:
            session.rollback()
            abort(400, message="Error while getting records Formular")

