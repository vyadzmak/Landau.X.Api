from db_models.modelsv2 import ChatMessages
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse, marshal
from sqlalchemy import or_, func
import threading
import modules.log_helper_module as log_module
import modules.db_helper as db_helper
import modules.socket_emitter as socket_emitter

message_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'chat_id': fields.Integer,
    'creation_date': fields.DateTime,
    'type': fields.Integer,
    'users_read': fields.List(fields.Integer),
    'content': fields.String
}


class ChatMessageResource(Resource):
    def __init__(self):
        self.route = "/v2/chatMessages/<int:id>"
        self.end_point = "v2-chat-messages"

    @marshal_with(message_fields)
    def get(self, id):
        try:
            messages = db_helper.get_item(ChatMessages, id)
            if not messages:
                abort(404, message="Chat message {} doesn't exist".format(id))
            return messages
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting Chat with id:{}".format(id))

    def delete(self, id):
        try:
            message = db_helper.delete_item(ChatMessages, id)
            if not message:
                abort(404, message="Chat message {} doesn't exist".format(id))
            return {}, 204
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error deleting chat message with id:{} doesn't exist".format(id))

    @marshal_with(message_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            message = db_helper.get_item(ChatMessages, id)
            if not message:
                abort(404, message="Chat message {} doesn't exist".format(id))
            message.users_read = message.users_read + list(set(json_data['users_read']) - set(message.users_read))
            session.add(message)
            session.commit()
            return message, 201
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            session.rollback()
            abort(400, message="Error while updating record Chat message")


class ChatMessageListResource(Resource):
    def __init__(self):
        self.route = "/v2/chatMessages"
        self.end_point = "v2-chat-messages-list"

    @marshal_with(message_fields)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id')
            parser.add_argument('chat_id')
            args = parser.parse_args()
            if len(args) == 0:
                abort(400, message='Arguments not found')
            id = args['id']
            chat_id = args['chat_id']
            messages = session.query(ChatMessages) \
                .filter(ChatMessages.chat_id == chat_id, or_(id == '-1', ChatMessages.id < int(id))) \
                .order_by(ChatMessages.id.desc()).limit(20).all()
            return messages

        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error in fetching chat messages")

    @marshal_with(message_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            json_data['users_read'] = [json_data['user_id']]
            message = db_helper.add_item(ChatMessages, json_data)

            socket_thread = threading.Thread(target=socket_emitter.emit,
                                             args=('new_message', marshal(message, message_fields)))
            socket_thread.start()

            return message, 201

        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            session.rollback()
            abort(400, message="Error in adding chat message")


class ChatMessageUnreadResource(Resource):
    def __init__(self):
        self.route = "/v2/unreadMessages"
        self.end_point = "v2-unread-messages"

    def post(self):
        try:
            json_data = request.get_json(force=True)
            messages = session.query(ChatMessages).filter(ChatMessages.id.in_(json_data['unread_messages'])).all()
            for message in messages:
                merged_list = list(set(message.users_read + [int(json_data['user_id'])]))
                message.users_read = merged_list
                session.add(message)
                session.commit()
            return '', 201
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            session.rollback()
            abort(400, message="Error in unread chat message")
