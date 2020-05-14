from flask_restful import Resource, fields, abort, reqparse
from models.client_product_model import ClientProduct
from db.db import session
from modules.json_serializator import encode_json
formular_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

parser = reqparse.RequestParser()

class ClientProductModelResource(Resource):
    def get(self, id):
        try:
            result = ClientProduct()
            result.init_empty_model(id)

            return encode_json(result)
        except Exception as e:
            session.rollback()
            abort(400, message="Error while deleting record products")

