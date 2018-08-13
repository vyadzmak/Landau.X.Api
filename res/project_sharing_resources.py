from db_models.models import ProjectSharing, Projects, ProjectAttachments, Users, Chats
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

import json

# user_fields = {
#     'id': fields.Integer,
#     'name': fields.String(attribute=lambda x: x.last_name + ' ' + x.first_name)
# }

project_sharing_fields = {
    'id': fields.Integer,
    'project_id': fields.Integer,
    'users_ids': fields.List(fields.Integer),
    # 'users': fields.List(fields.Nested(user_fields))
}


class ProjectSharingResource(Resource):
    @marshal_with(project_sharing_fields)
    def get(self, id):
        sharing = session.query(ProjectSharing) \
            .filter(ProjectSharing.project_id == id).first()
        if not sharing:
            abort(404, message="Project sharing {} doesn't exist".format(id))
        return sharing

    @marshal_with(project_sharing_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            sharing = session.query(ProjectSharing).filter(ProjectSharing.id == id).first()

            sharing.users_ids = json_data["users_ids"]
            session.add(sharing)
            session.commit()

            project = session.query(Projects).filter(Projects.id == sharing.project_id).first()
            project_creator = session.query(Users).filter(Users.id == project.user_id).first()
            chats = session.query(Chats).filter(Chats.project_id == project.id,
                                                Chats.creator_id == project_creator.id).all()

            users = session.query(Users).filter(Users.id.in_(json_data["users_ids"])).all()
            risks = filter(lambda x: x.user_role_id == 7, users)

            attachments = session.query(ProjectAttachments) \
                .filter(ProjectAttachments.project_id == sharing.project_id,
                        ProjectAttachments.is_removed == False).all()

            if attachments is not None:
                for attachment in attachments:
                    user_ids = set(attachment.user_ids or []) & set(json_data["users_ids"])
                    if risks is not None:
                        user_ids |= set([x.id for x in risks])
                    attachment.user_ids = list(user_ids)
                    session.add(attachment)
                    session.commit()
            for user in users:
                chat_needed = True
                for chat in chats:
                    if len(chat.user_ids) == 1 and chat.user_ids[0] == user.id:
                        chat_needed = False
                if chat_needed:
                    chat_name = '{}.{}//{}.{}'.format(project_creator.first_name[:1], project_creator.last_name,
                                                      user.first_name[:1], user.last_name)
                    chat = Chats(chat_name, project_creator.id, project.id, [user.id])
                    session.add(chat)
                    session.commit()


            return sharing, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while updating record Project Sharing")


class ProjectSharingListResource(Resource):
    @marshal_with(project_sharing_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            sharing = ProjectSharing(project_id=json_data["project_id"],
                                     users_ids=json_data["users_ids"])

            session.add(sharing)
            session.commit()

            project = session.query(Projects).filter(Projects.id == sharing.project_id).first()
            project_creator = session.query(Users).filter(Users.id == project.user_id).first()
            chats = session.query(Chats).filter(Chats.project_id == project.id,
                                                Chats.creator_id == project_creator.id).all()

            users = session.query(Users).filter(Users.id.in_(json_data["users_ids"])).all()
            risks = filter(lambda x: x.user_role_id == 7, users)

            attachments = session.query(ProjectAttachments) \
                .filter(ProjectAttachments.project_id == sharing.project_id,
                        ProjectAttachments.is_removed == False).all()

            if attachments is not None:
                for attachment in attachments:
                    user_ids = set(attachment.user_ids or []) & set(json_data["users_ids"])
                    if risks is not None:
                        user_ids |= set([x.id for x in risks])
                    attachment.user_ids = list(user_ids)
                    session.add(attachment)
                    session.commit()
            for user in users:
                chat_needed = True
                for chat in chats:
                    if len(chat.user_ids) == 1 and chat.user_ids[0] == user.id:
                        chat_needed = False
                if chat_needed:
                    chat_name = '{}.{}//{}.{}'.format(project_creator.first_name[:1], project_creator.last_name,
                                                      user.first_name[:1], user.last_name)
                    chat = Chats(chat_name, project_creator.id, project.id, [user.id])
                    session.add(chat)
                    session.commit()

            return sharing, 201
            # return "OK"
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Project Sharing")
