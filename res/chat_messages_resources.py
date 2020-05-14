from db_models.models import ChatMessages
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse, marshal
from sqlalchemy import or_, func
import threading
import modules.log_helper_module as log_module
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
    @marshal_with(message_fields)
    def get(self, id):
        messages = session.query(ChatMessages).filter(ChatMessages.id == id).first()
        if not messages:
            abort(404, message="Chat message {} doesn't exist".format(id))
        return messages

    def delete(self, id):
        message = session.query(ChatMessages).filter(ChatMessages.id == id).first()
        if not message:
            abort(404, message="Chat message {} doesn't exist".format(id))
        session.delete(message)
        session.commit()
        return {}, 204

    @marshal_with(message_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            message = session.query(ChatMessages).filter(ChatMessages.id == id).first()
            message.users_read = message.users_read + list(set(json_data['users_read']) - set(message.users_read))
            session.add(message)
            session.commit()
            return message, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while updating record Chat message")


class ChatMessageListResource(Resource):
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
            log_module.add_log("Fetch chat messages error. " + str(e))
            abort(400, message="Error in fetching chat messages")

    @marshal_with(message_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            users_read = [json_data['user_id']]
            message = ChatMessages(json_data['content'], json_data['user_id'], json_data['chat_id'], json_data['type'],
                                   users_read)
            session.add(message)
            session.commit()

            # socket_thread = threading.Thread(target=socket_emitter.emit,
            #                                  args=('new_message', marshal(message, message_fields)))
            # socket_thread.start()
            # try:
            #     with SocketIO(app_settings.SOCKET_URL, 8000, LoggingNamespace, wait_for_connection=False) as socketIO:
            #         socketIO.emit('new_message', marshal(message, message_fields))
            #         socketIO.wait(seconds=0)
            # except Exception as e:
            #     log_module.add_log("Add chat message error. " + str(e))

            # with concurrent.futures.ThreadPoolExecutor(max_workers=2):
            #     try:
            #         with SocketIO(app_settings.SOCKET_URL, 8000, LoggingNamespace, wait_for_connection=False) as socketIO:
            #             socketIO.emit('new_message', marshal(message, message_fields))
            #             socketIO.close()
            #     except Exception as e:
            #         log_module.add_log("Add chat message error. " + str(e))

            return message, 201

        except Exception as e:
            log_module.add_log("Add chat message error. " + str(e))
            session.rollback()
            abort(400, message="Error in adding chat message")


class ChatMessageUnreadResource(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            # session.query(ChatMessages) \
            #     .filter(ChatMessages.id.in_(json_data['unread_messages']))\
            #     .update({ChatMessages.users_read: array_cat(ChatMessages.users_read, json_data['user_id'])})

            messages = session.query(ChatMessages).filter(ChatMessages.id.in_(json_data['unread_messages'])).all()
            for message in messages:
                merged_list = list(set(message.users_read + [int(json_data['user_id'])]))
                message.users_read = merged_list
                session.add(message)
                session.commit()
            return '', 201
        except Exception as e:
            log_module.add_log("Add chat message error. " + str(e))
            session.rollback()
            abort(400, message="Error in adding chat message")
