from db_models.models import Chats, Users, ChatMessages
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import or_, func
import modules.log_helper_module as log_module

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
    @marshal_with(chat_fields)
    def get(self, id):
        chat = session.query(Chats).filter(Chats.id == id).first()
        chat.users = session.query(Users).filter(Users.id.in_(chat.user_ids)).all()
        if not chat:
            abort(404, message="Chat {} doesn't exist".format(id))
        return chat

    def delete(self, id):
        chat = session.query(Chats).filter(Chats.id == id).first()
        if not chat:
            abort(404, message="Chat {} doesn't exist".format(id))
        session.delete(chat)
        session.commit()
        return {}, 204

    @marshal_with(chat_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            chat = session.query(Chats).filter(Chats.id == id).first()
            chat.name = json_data['name']
            chat.user_ids = json_data['user_ids']
            session.add(chat)
            session.commit()
            return chat, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while updating record Chat")


class ChatListResource(Resource):
    @marshal_with(chat_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id')
        parser.add_argument('project_id')
        args = parser.parse_args()
        if len(args) == 0:
            abort(400, message='Arguments not found')
        user_id = args['user_id']
        project_id = args['project_id']

        chats = session.query(Chats) \
            .filter(Chats.project_id == project_id,
                    or_(Chats.creator_id == user_id, Chats.user_ids.any(user_id))) \
            .all()
        # !!! here is very bad code
        for chat in chats:
            if len(chat.messages)>0:
                chat.unread_count = len([x.id for x in chat.messages if int(user_id) not in x.users_read])
                chat.last_message = chat.messages[-1]
        return chats

    @marshal_with(chat_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            chat = Chats(json_data['name'], json_data['creator_id'], json_data['project_id'], json_data['user_ids'])
            session.add(chat)
            session.commit()
            return chat, 201
        except Exception as e:
            log_module.add_log("Add chat error. " + str(e))
            session.rollback()
            abort(400, message="Error in adding chat Role")
