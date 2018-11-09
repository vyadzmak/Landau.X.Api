from db_models.modelsv2 import ReportHistory, Reports, ReportAudit
from db.db import session
from flask_restful import Resource, marshal_with, abort, reqparse
from sqlalchemy.orm import contains_eager
import modules.log_helper_module as log_module
import modules.report_data_refiner as data_refiner
from resv2.report_history_resources import \
    data_fields as history_data_fields, user_name_fields as history_user_name, report_audit_fields as report_audit

output_project_report_history_fields = {**history_data_fields, **history_user_name, **report_audit}
output_project_report_history_fields.pop('data', None)


class ProjectReportHistoryResource(Resource):
    def __init__(self):
        self.route = "/v2/projectReportHistory/<int:id>"
        self.end_point = "v2-project-report-history-by-project"

    @marshal_with(history_data_fields)
    def get(self, id):
        try:
            report = session.query(ReportHistory).filter(ReportHistory.project_id == id) \
                .order_by(ReportHistory.id.desc()).first()
            if not report:
                report_t = session.query(Reports).filter(Reports.project_id == id).first()
                compressed_data = data_refiner.compress_data(report_t.data)
                report = ReportHistory(project_id=id,
                                       data=compressed_data,
                                       user_id=None)
                session.add(report)
                session.commit()
            return report
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting {} with project_id:{}".format(self.route, id))

class ProjectReportHistoryListResource(Resource):
    def __init__(self):
        self.route = "/v2/projectReportHistoryList"
        self.end_point = "v2-project-report-history-list-by-project"

    @marshal_with(output_project_report_history_fields)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('project_id')
            parser.add_argument('user_id')
            args = parser.parse_args()
            if len(args) == 0:
                abort(400, message='Arguments not found')
            project_id = args['project_id']
            user_id = args['user_id']

            subq = session.query(ReportAudit). \
                filter(ReportAudit.history_id == ReportHistory.id). \
                order_by(ReportAudit.is_system.desc(), ReportAudit.type_id). \
                limit(10).subquery().lateral()

            reports = session.query(ReportHistory).outerjoin(subq) \
                .filter(ReportHistory.project_id == project_id) \
                .options(contains_eager(ReportHistory.report_audit_data, alias=subq)) \
                .all()

            if not reports:
                abort(404, message="Report History not found")
            return reports
        except Exception as e:
            log_module.add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, message="Error while getting {} with project_id:{}".format(self.route, project_id))
