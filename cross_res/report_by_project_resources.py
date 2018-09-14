from db_models.models import Reports
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.log_helper_module as log_module
from resv2.reports_resources import OUTPUT_FIELDS


class ProjectReportResource(Resource):
    def __init__(self):
        self.route = "/v2/projectReport/<int:id>"
        self.end_point = "v2-project-report-by-project"

    @marshal_with(OUTPUT_FIELDS)
    def get(self, id):
        try:
            report = session.query(Reports).filter(Reports.project_id == id).first()
            if not report:
                abort(404, message="Reports not found")
            return report
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting Project Report with project_id:{}".format(id))
