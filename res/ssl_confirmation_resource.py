from flask import Flask, jsonify, request,send_from_directory
from flask_restful import Resource, fields, marshal_with, abort, reqparse

import settings
#PARAMS
ENTITY_NAME = "SSL Confirmation"
#MODEL = Settings
# ROUTE ="/.well-known/acme-challenge"
# END_POINT = "ssl-confirmation"


#API METHODS FOR SINGLE ENTITY
class SSLConfirmationResource(Resource):
    # def __init__(self):
    #     # self.route = ROUTE+'/<path:file>'
    #     # self.end_point = END_POINT
    #     pass

    def get(self, file):
        try:
            w ='.well-known'
            a= 'acme-challenge'
            file_path =settings.ROOT_DIR.replace("\\","/")+"/"+w+"/"+a

            return send_from_directory(file_path,file)
        except Exception as e:
            abort(404, message="File not found")

