from db_models.models import ProjectControlLog, Projects
from db.db import session
from flask_restful import Resource, marshal_with, abort
from resv2.project_control_log_resources import OUTPUT_FIELDS
import modules.log_helper_module as log_module


class ProjectSelectControlLogResource(Resource):
    def __init__(self):
        self.route = "/v2/projectSelectControlLog/<int:id>"
        self.end_point = "v2-project-select-control-log"
    @marshal_with(OUTPUT_FIELDS)
    def get(self, id):
        try:
            log = session.query(ProjectControlLog).filter(ProjectControlLog.project_id == id).first()
            if not log:
                abort(404, message="Log not found")
            return log
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting Project Select Control Log with project_id:{}".format(id))