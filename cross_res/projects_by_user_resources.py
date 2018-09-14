from db_models.modelsv2 import Projects, ProjectSharing
from db.db import session
from flask import Flask, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.log_helper_module as log_module
from resv2.projects_resources import OUTPUT_FIELDS

#PARAMS
ENTITY_NAME = "Projects by User"
MODEL = Projects
ROUTE ="/v2/userProjects/<int:id>"
END_POINT = "v2-projects-by-user"


class UserProjectListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(OUTPUT_FIELDS)
    def get(self, id):
        try:
            action_type = 'GET'
            log_module.log_user_actions(ROUTE, id, action_type)
            user_projects = session.query(MODEL).filter(MODEL.user_id == id)
            shared_projects = session.query(MODEL) \
                        .join(ProjectSharing, MODEL.id == ProjectSharing.project_id) \
                        .filter(ProjectSharing.users_ids.any(id))
            projects = user_projects.union(shared_projects).distinct().all()
            if not projects:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            return projects
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Неопознанная ошибка")

