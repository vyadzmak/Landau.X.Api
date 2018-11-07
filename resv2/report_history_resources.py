from db_models.modelsv2 import ReportHistory
from flask_restful import Resource, fields

from db.db import session
from modules.report_audit_comparer import get_diffs
import modules.report_data_refiner as data_refiner
from modules.json_serializator import decode
import json
import objectpath

# PARAMS
NAME = "ReportHistoryResource"
NAME_LIST = "ReportHistoryListResource"
ENTITY_NAME = "ReportHistory"
MODEL = ReportHistory
ROUTE = "/v2/reportHistory"
END_POINT = "v2-report-history"
ROUTE_LIST = ROUTE
END_POINT_LIST = END_POINT + "-list"
# SCHEMA FIELDS
data_fields = {
    'id': fields.Integer(attribute="id"),
    'project_id': fields.Integer(attribute="project_id"),
    'user_id': fields.Integer(attribute="user_id"),
    'date': fields.DateTime(attribute="date"),
    'data': fields.String(attribute=lambda x: data_refiner.decompress_data(x.data))
}

# NESTED SCHEMA FIELDS
user_name = {
    'user_name': fields.String(
        attribute=lambda x: x.user_data.first_name + " " + x.user_data.last_name if x.user_data else "Cистема")
}
# OUTPUT SCHEMA
OUTPUT_FIELDS = {**data_fields}


def post_data_converter(json_data):
    previous_report = session.query(ReportHistory).filter(ReportHistory.project_id == json_data["project_id"]) \
        .order_by(ReportHistory.id.desc()).first()
    if not previous_report:
        raise Exception('Previous report has not been found! Unable to check versions.')
    previous_report_data = data_refiner.decompress_data(previous_report.data)
    report_t = session.query(Reports).filter(Reports.project_id == json_data["project_id"]).first()
    if not report_t:
        raise Exception('Previous report from Reports table has not been found! Unable to check versions.')
    analytic_rule_id = report_t.analytic_rule_id

    rules_data = session.query(AnalyticRules).filter(AnalyticRules.id == analytic_rule_id).first()
    tree_obj = objectpath.Tree(decode(rules_data.data))
    rules_data = list(tree_obj.execute('$..conditions.(str(code), name)'))
    rules_data += list(tree_obj.execute('$..opiu_cards_formulas.(str(code), name)'))
    rules_data += list(tree_obj.execute('$..odds_formulas.(str(code), name)'))
    rules_data += list(tree_obj.execute('$..balance_formulas.(str(code), name)'))
    rules_data = {x['code']: x['name'] for x in rules_data}

    # add hex keys to json_data new cells
    report_data = data_refiner.add_uids(json_data['data'])

    diffs = get_diffs(previous_report_data, report_data, rules_data)
    diffs = [ReportAudit(None, diff['type_id'], diff['operation_id'], diff['is_system'], diff['text'])
             for diff in diffs]
    if len(diffs) == 0:
        abort(404, message="There are no differences between documents")
    # delete timestamp props and other from json json_data["data"]
    report_data = data_refiner.delete_unused_props(report_data)
    report_data = data_refiner.compress_data(report_data)

    json_data['data'] = report_data
    json_data['report_audit_data'] = diffs
    return json_data