from db_models.modelsv2 import ProjectAnalysisLog
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort
from modules.json_serializator import engine_encode, engine_decode
from modules.log_helper_module import add_log
from resv2.project_analysis_log_resources import OUTPUT_FIELDS

# PARAMS
ENTITY_NAME = "Project Analysis Log By Project"
MODEL = ProjectAnalysisLog
ROUTE = "/v2/projectSelectAnalysisLog/<int:id>"
END_POINT = "v2-project-select-analysis-log"

class ProjectSelectAnalysisLogResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(OUTPUT_FIELDS)
    def get(self, id):
        try:
            log = session.query(MODEL).filter(MODEL.project_id == id).first()
            if not log:
                abort(404, message="Analysis Log not found")
            return log
        except Exception as e:
            abort(400, message="Error while getting {0} with id:{1}".format(ENTITY_NAME, id))
