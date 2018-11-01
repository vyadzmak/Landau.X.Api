from db_models.modelsv2 import Chats, Users, ChatMessages
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import or_, func
from sqlalchemy.orm import Load
import modules.log_helper_module as log_module
import modules.db_helper as db_helper

user_fields = {
    'id': fields.Integer,
    'name': fields.String(attribute=lambda x: x.last_name + ' ' + x.first_name)
}

message_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'chat_id': fields.Integer,
    'creation_date': fields.DateTime,
    'type': fields.Integer,
    'users_read': fields.List(fields.Integer),
    'content': fields.String
}

chat_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'creator_id': fields.Integer,
    'project_id': fields.Integer,
    'is_open': fields.Boolean,
    'unread_count': fields.Integer,
    'last_message': fields.Nested(message_fields)
}

chat_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'creator_id': fields.Integer,
    'project_id': fields.Integer,
    'is_open': fields.Boolean,
    'user_ids': fields.List(fields.Integer),
    'user_data': fields.Nested(user_fields),
    'users': fields.List(fields.Nested(user_fields))
}


class ChatResource(Resource):
    def __init__(self):
        self.route = "/v2/chats/<int:id>"
        self.end_point = "v2-chats"

    @marshal_with(chat_fields)
    def get(self, id):
        try:
            chat = db_helper.get_item(Chats, id)
            if not chat:
                abort(404, message="Chat {} doesn't exist".format(id))
            chat.users = session.query(Users).filter(Users.id.in_(chat.user_ids)).all()

            return chat
        except Exception as e:
            session.rollback()
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting Chat with id:{}".format(id))

    def delete(self, id):
        try:
            chat = db_helper.delete_item(Chats, id)
            if chat is None:
                abort(404, message="Chat {} doesn't exist".format(id))
            return {}, 204
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error deleting chat with id:{} doesn't exist".format(id))

    @marshal_with(chat_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            chat = db_helper.update_item(Chats, json_data, id)
            return chat, 201
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while updating record Chat with id:{}".format(id))


class ChatListResource(Resource):
    def __init__(self):
        self.route = "/v2/chats"
        self.end_point = "v2-chats-list"

    @marshal_with(chat_list_fields)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            parser.add_argument('project_id')
            args = parser.parse_args()
            if len(args) == 0:
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            project_id = args['project_id']

            chats = session.query(Chats) \
                .filter(Chats.project_id == project_id, or_(Chats.is_open == None, Chats.is_open == False),
                        or_(Chats.creator_id == user_id, Chats.user_ids.any(user_id))) \
                .all()
            # !!! here is very bad code
            for chat in chats:
                if len(chat.messages) > 0:
                    chat.unread_count = len([x.id for x in chat.messages if int(user_id) not in x.users_read])
                    chat.last_message = chat.messages[-1]
            return chats
        except Exception as e:
            session.rollback()
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting Chat with user_id:{0}, project_id:{1}".format(user_id, project_id))

    @marshal_with(chat_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            chat = db_helper.add_item(Chats, json_data)
            return chat, 201
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error in adding Chat")
