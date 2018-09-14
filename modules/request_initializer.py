from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.log_helper_module as log_module
import modules.db_helper as db_helper


# CREATING INIT METHOD
def create_init(route, end_point):
    def __init__(self):
        self.route = route
        self.end_point = end_point
        pass

    return __init__


# API METHODS FOR SINGLE ENTITY
def create_get(entity_name, model, output_fields):
    @marshal_with(output_fields)
    def get(self, id):
        try:
            entity = db_helper.get_item(model, id)
            if entity is None:
                abort(404, message="{0} with id:{1} doesn't exist".format(entity_name, id))
            return entity
        except Exception as e:
            log_module.add_log("Error while getting {0} with id:{1} - {2}".format(entity_name, id, e))
            abort(400, message="Error while getting {0} with id:{1}".format(entity_name, id))
        finally:
            pass

    return get


def create_delete(entity_name, model):
    def delete(self, id):
        try:
            entity = db_helper.delete_item(model, id)
            if entity is None:
                abort(404, message="{0} with id:{1} doesn't exist".format(entity_name, id))
            return {}, 200  # 204
        except Exception as e:
            log_module.add_log("Error while removing {0} with id:{1} - {2}".format(entity_name, id, e))
            abort(400, message="Error while remove " + entity_name)

    return delete


def create_put(entity_name, model, output_fields, input_data_converter, after_put_action):
    @marshal_with(output_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            if input_data_converter is not None:
                json_data = input_data_converter(json_data)
            entity = db_helper.update_item(model, json_data, id)
            if entity is None:
                abort(404, message="{0} with id:{1} doesn't exist".format(entity_name, id))
            if after_put_action is not None:
                after_put_action(entity, json_data)
            return entity, 200 # 201
        except Exception as e:
            log_module.add_log("Error while updating {0} with id:{1} - {2}".format(entity_name, id, e))
            abort(400, message="Error while update " + entity_name)

    return put


# API METHODS FOR LIST ENTITIES
def create_get_list(entity_name, model, output_fields):
    @marshal_with(output_fields)
    def get(self):
        try:
            entities = db_helper.get_items(model)
            return entities
        except Exception as e:
            log_module.add_log("Error while getting list of {0} - {2}".format(entity_name, e))
            abort(400, message="Error while getting list of {}".format(entity_name))

    return get


def create_post(entity_name, model, output_fields, input_data_converter, after_post_action):
    @marshal_with(output_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            if input_data_converter is not None:
                json_data = input_data_converter(json_data)
            entity = db_helper.add_item(model, json_data)
            if after_post_action is not None:
                after_post_action(entity, json_data)
            return entity, 201
        except Exception as e:
            log_module.add_log("Error while adding record of {0} - {2}".format(entity_name, e))
            abort(400, message="Error while adding record " + entity_name)

    return post
