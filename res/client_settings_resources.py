from db_models.models import Users, Clients, ClientSettings
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import and_
from models.client_settings_model import ClientSettingsModel
from modules.json_serializator import encode_json
from flask import Flask, jsonify, request
import json
class ClientSettingsResource(Resource):

    def get(self, id):
        try:
            client_settings = session.query(ClientSettings).filter(
                ClientSettings.client_id == id) \
                .first()
            result  =None
            if (client_settings==None):
                client_settings = ClientSettings(id,1)
                session.add(client_settings)
                session.commit()

            result = ClientSettingsModel()
            result.client_id = client_settings.client_id
            result.id = client_settings.id
            result.engine_number = client_settings.engine_number
            result.show_products_form = client_settings.show_products_form
            result.show_project_error_states = client_settings.show_project_error_states
            result.show_project_registration_number_column = client_settings.show_project_registration_number_column



            if not result:
                abort(404, message="Client settings not found")
            return encode_json(result)
        except Exception as e:
            abort(400, message="Bad request")

    def put(self, id):
        try:
            json_data = request.get_json(force=True)


            client_settings = session.query(ClientSettings).filter(ClientSettings.id == id).first()
            client_settings.engine_number = json_data["engine_number"]
            client_settings.show_products_form = json_data["show_products_form"]
            client_settings.show_project_error_states = json_data["show_project_error_states"]
            client_settings.show_project_registration_number_column = json_data["show_project_registration_number_column"]
            session.add(client_settings)
            session.commit()

            result = ClientSettingsModel()
            result.client_id = client_settings.client_id
            result.id = client_settings.id
            result.engine_number = client_settings.engine_number
            result.show_products_form = client_settings.show_products_form
            result.show_project_error_states = client_settings.show_project_error_states
            result.show_project_registration_number_column = client_settings.show_project_registration_number_column


            return encode_json(result),201

        except Exception as e:
            abort(400, message="Bad request")