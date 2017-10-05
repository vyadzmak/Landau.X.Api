from db_models.models import ClientTypes
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort,reqparse

client_type_fields = {
    'id': fields.Integer,
    'name': fields.String
}

parser = reqparse.RequestParser()

class ClientTypeResource(Resource):
    @marshal_with(client_type_fields)
    def get(self, id):
        client_type = session.query(ClientTypes).filter(ClientTypes.id == id).first()
        if not client_type:
            abort(404, message="Client type {} doesn't exist".format(id))
        return client_type

    def delete(self, id):
        client_type = session.query(ClientTypes).filter(ClientTypes.id == id).first()
        if not client_type:
            abort(404, message="Client type {} doesn't exist".format(id))
        session.delete(client_type)
        session.commit()
        return {}, 204

    @marshal_with(client_type_fields)
    def put(self, id):

        json_data = request.get_json(force=True)
        client_type = session.query(ClientTypes).filter(ClientTypes.id == id).first()
        client_type.name = json_data['name']
        session.add(client_type)
        session.commit()
        return client_type, 201

class ClientTypeListResource(Resource):
    @marshal_with(client_type_fields)
    def get(self):
        client_types = session.query(ClientTypes).all()
        return client_types

    @marshal_with(client_type_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            client_type= ClientTypes(name=json_data["name"])
            session.add(client_type)
            session.commit()
            return client_type, 201
        except Exception as e:
            abort(400, message="Error while adding record Client Type")