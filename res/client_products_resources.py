from flask import request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

from db.db import session
from db_models.models import Products
from models.client_product_model import ClientProduct
from modules.json_serializator import encode_json
client_product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'creation_date':fields.DateTime

}

parser = reqparse.RequestParser()


class ClientProductsResource(Resource):
    def get(self,id):
        client_product = session.query(Products).filter(Products.id == id).first()
        if not client_product:
            abort(404, message="client_product {} doesn't exist".format(id))
        result = ClientProduct()
        result.init_empty_model(client_product.user_creator_id)
        result.schema_id = client_product.schema_id
        result.name = client_product.name
        result.formular_id =client_product.formular_id
        result.user_id = client_product.user_creator_id
        result.client_id = client_product.client_id
        result.creation_date = client_product.creation_date
        return encode_json(result)


    def put(self, id):
        json_data = request.get_json(force=True)
        schema_id = json_data['schema_id']
        formular_id = json_data['formular_id']
        name = json_data['name']
        client_product = session.query(Products).filter(Products.id == id).first()
        client_product.name = name
        client_product.formular_id = formular_id
        client_product.schema_id = schema_id
        session.add(client_product)
        session.commit()
        result = ClientProduct()
        result.id = client_product.id
        result.init_empty_model(client_product.user_creator_id)
        result.schema_id = client_product.schema_id
        result.name = client_product.name
        result.formular_id = client_product.formular_id
        result.user_id = client_product.user_creator_id
        result.client_id = client_product.client_id
        result.creation_date = str(client_product.creation_date)
        return encode_json(result)

    def delete(self, id):
        try:
            product = session.query(Products).filter(Products.id == id).first()
            if not product:
                abort(404, message="Product {} doesn't exist".format(id))
            session.delete(product)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while deleting record products")


class ClientProductsListResource(Resource):
    @marshal_with(client_product_fields)
    def get(self, id):
        try:
            client_products = session.query(Products).filter(Products.client_id == id).all()
            return client_products
        except Exception as e:
            session.rollback()
            abort(400, message="Error while getting records Formular")

    @marshal_with(client_product_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            client_id = json_data['client_id']
            user_id = json_data['user_id']
            schema_id = json_data['schema_id']
            formular_id = json_data['formular_id']
            name = json_data['name']
            client_product = Products(client_id,user_id,schema_id,formular_id,name)
            session.add(client_product)
            session.commit()
            return client_product, 201
        except Exception as e:
            abort(400, message="Error while adding record Project")
