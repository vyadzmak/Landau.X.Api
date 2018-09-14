from db_models.modelsv2 import ProjectAnalysis, ProjectControlLog, ReportForms
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort
from modules.json_serializator import engine_encode, engine_decode
from modules.log_helper_module import add_log
from resv2.project_analysis_resources import OUTPUT_FIELDS as parent_fields

# PARAMS
ENTITY_NAME = "Project Analysis By Project"
MODEL = ProjectAnalysis
ROUTE = "/v2/projectSelectAnalysis/<int:id>"
END_POINT = "v2-project-select-analysis"

class LogItems(fields.Raw):
    def format(self, value):
        if value is None or value == '':
            return {'success': 0, 'warning': 0, 'error': 0, 'info': 0}
        json_ob = engine_decode(value)
        result = {
            'success': len([x for x in json_ob if x['state_id'] == 1]),
            'warning': len([x for x in json_ob if x['state_id'] == 2]),
            'error': len([x for x in json_ob if x['state_id'] == 3]),
            'info': len([x for x in json_ob if x['state_id'] == 4]),
            'engine_operations': len([x for x in json_ob if x['state_id'] == 5])
        }
        return result


OUTPUT_FIELDS = dict(parent_fields)
OUTPUT_FIELDS['log'] = LogItems(attribute='pc_data')

class ProjectAnalysisRemover(Resource):
    def __init__(self):
        self.route = "/v2/projectCleanData/<int:id>"
        self.end_point = "v2-project-clean-data"
        pass

    def delete(self, id):
        try:
            session.query(MODEL).filter(MODEL.project_id == id).delete(synchronize_session=False)
            session.commit()

            session.query(ReportForms).filter(ReportForms.project_id == id).delete(synchronize_session=False)
            session.commit()

            # if not analysis:
            #     abort(404, message="Document {} doesn't exist".format(id))
            # session.delete(analysis)
            # session.commit()
            return {}, 204
        except Exception as e:
            add_log("Error while removing {0} with id: {1}".format(ENTITY_NAME, id))
            abort(400, message="Error while removing {0} with id: {1}".format(ENTITY_NAME, id))


class ProjectSelectAnalysisResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(OUTPUT_FIELDS)
    def get(self, id):
        try:
            analysis = session.query(MODEL) \
                .join(ProjectControlLog, ProjectControlLog.project_id == MODEL.project_id) \
                .add_columns(MODEL.id, MODEL.project_id, MODEL.data,
                             ProjectControlLog.id.label('pc_id'), ProjectControlLog.data.label('pc_data')) \
                .filter(MODEL.project_id == id).first()
            if not analysis:
                abort(404, message="Reports not found")
            return {
                'id': analysis.id,
                'data': analysis.data,
                'project_id': analysis.project_id,
                'pc_data': analysis.pc_data
            }
        except Exception as e:
            abort(400, message="Error while adding record Document")
