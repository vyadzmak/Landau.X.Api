from db_models.modelsv2 import ProjectSharing, Projects, ProjectAttachments, Users, Chats
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_helper as db_helper
import modules.log_helper_module as log_module

import json

# PARAMS
ENTITY_NAME = "Project Sharing"
MODEL = ProjectSharing
ROUTE = "/v2/projectSharing"
END_POINT = "v2-project-sharing"

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
    def __init__(self):
        self.route = ROUTE + "/<int:id>"
        self.end_point = END_POINT
        pass

    @marshal_with(project_sharing_fields)
    def get(self, id):
        try:
            sharing = session.query(MODEL) \
                .filter(MODEL.project_id == id).first()
            if not sharing:
                abort(404, message="Project sharing {} doesn't exist".format(id))
            return sharing
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Неопознанная ошибка")

    @marshal_with(project_sharing_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            sharing = db_helper.update_item(MODEL, json_data, id)
            if sharing is None:
                abort(404, message="{0} with id:{1} doesn't exist".format(ENTITY_NAME, id))

            project = sharing.project_data
            project_creator = project.user_data
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
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while updating record Project Sharing")


class ProjectSharingListResource(Resource):
    def __init__(self):
        self.route = ROUTE + "s"
        self.end_point = END_POINT + "s"
        pass

    @marshal_with(project_sharing_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            sharing = MODEL(project_id=json_data["project_id"],
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
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while adding record Project Sharing")
