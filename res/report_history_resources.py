from db_models.models import Projects, ReportHistory, Reports, ReportAuditTypes, ReportOperations, ReportAudit, \
    AnalyticRules
from db.db import session
from sqlalchemy.orm import contains_eager
from flask import Flask, jsonify, request, make_response,send_from_directory,send_file
from flask_restful import Resource, fields, marshal_with, abort, reqparse, marshal
from modules.report_audit_comparer import get_diffs
import modules.report_data_refiner as data_refiner
from modules.json_serializator import decode
import json
import objectpath
from modules.threadpool import threadpool
from pathlib import Path
from res.report_audit_resources import output_fields as report_audit_fields

output_fields = {
    'id': fields.Integer,
    'date': fields.DateTime,
    'data': fields.String(attribute=lambda x: data_refiner.decompress_data(x.data)),
    'project_id': fields.Integer,
    'user_id': fields.Integer
}

output_project_report_history_fields = {
    'id': fields.Integer,
    'date': fields.DateTime,
    'project_id': fields.Integer,
    'user_id': fields.Integer,
    'user_name': fields.String(
        attribute=lambda x: x.user_data.first_name + " " + x.user_data.last_name if x.user_data else "Cистема"),
    'report_audit': fields.Nested(report_audit_fields, attribute='report_audit_data')
}

import jsonpickle


def encode(ob):
    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)
        # jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        json_s = jsonpickle.encode(ob, unpicklable=True)
        return json_s
    except Exception as e:
        print(str(e))
        return ""


class ProjectReportHistoryResource(Resource):
    @marshal_with(output_fields)
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
            abort(400, message=repr(e))


class NewProjectReportHistoryResource(Resource):

    def get(self, id):
        try:
            report = session.query(ReportHistory).filter(ReportHistory.project_id == id) \
                .order_by(ReportHistory.id.desc()).first()

            data = decode(report.data)

            if (data==''):
                report = session.query(Reports).filter(Reports.project_id==id).first()
                data = decode(report.data)
                file_path = decode(data)
                p = Path(file_path['file_path'])
                file_name = str(p.name)
                dir_name = str(p.parent)


                return send_from_directory(dir_name, file_name, as_attachment=True)
            t = 0


            return None
        except Exception as e:
            abort(400, message=repr(e))
class ProjectReportHistoryListResource(Resource):
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

            reports = session.query(ReportHistory).outerjoin(subq)\
                .filter(ReportHistory.project_id == project_id)\
                .options(contains_eager(ReportHistory.report_audit_data, alias=subq))\
                .all()

            # reports = session.query(ReportHistory).filter(ReportHistory.project_id == project_id).all()
            if not reports:
                abort(404, message="Report History not found")
            return reports
        except Exception as e:
            abort(400, message=repr(e))

class ReportHistoryResource(Resource):
    @marshal_with(output_fields)
    def get(self, id):
        try:
            report = session.query(ReportHistory).filter(ReportHistory.id == id).first()
            if not report:
                abort(404, message="Report History {} doesn't exist".format(id))
            return report
        except Exception as e:
            abort(400, message=repr(e))

    def delete(self, id):
        try:
            report = session.query(ReportHistory).filter(ReportHistory.id == id).first()
            if not report:
                abort(404, message="Report History {} doesn't exist".format(id))
            session.delete(report)
            session.commit()
            return {}, 204
        except Exception as e:
            abort(400, message=repr(e))

    @marshal_with(output_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            report = session.query(ReportHistory).filter(ReportHistory.id == id).first()
            report.data = json_data["data"]
            report.user_id = json_data["user_id"]
            report.project_id = json_data["project_id"]
            report.date = json_data["date"]
            session.add(report)
            session.commit()
            return report, 201
        except Exception as e:
            abort(400, message=repr(e))


@threadpool
def post_task1(project_id):
    previous_report = session.query(ReportHistory).filter(ReportHistory.project_id == project_id) \
        .order_by(ReportHistory.id.desc()).first()
    if not previous_report:
        raise Exception('Previous report has not been found! Unable to check versions.')
    return data_refiner.decompress_data(previous_report.data)


@threadpool
def post_task3(data):
    # add hex keys to json_data new cells
    return data_refiner.add_uids(data)


@threadpool
def post_task2(project_id):
    report_t = session.query(Reports).filter(Reports.project_id == project_id).first()
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
    return rules_data


class ReportHistoryListResource(Resource):
    @marshal_with(output_fields)
    def get(self):
        try:
            reports = session.query(ReportHistory).all()
            return reports
        except Exception as e:
            abort(400, message=str(e))

    # @marshal_with(output_fields)
    def post(self):
        try:

            json_data = request.get_json(force=True)
            previous_report_data = post_task1(json_data["project_id"])
            rules_data = post_task2(json_data["project_id"])
            report_data = post_task3(json_data["data"])

            previous_report_data = previous_report_data.result()
            rules_data = rules_data.result()
            report_data = report_data.result()

            diffs = get_diffs(previous_report_data, report_data, rules_data)
            diffs = [ReportAudit(None, diff['type_id'], diff['operation_id'], diff['is_system'], diff['text'], diff.get('uid', ''))
                     for diff in diffs]
            if len(diffs) == 0:
                abort(404, message="There are no differences between documents")
            # delete timestamp props and other from json json_data["data"]
            report_data = data_refiner.delete_unused_props(report_data)
            report_data = data_refiner.compress_data(report_data)

            report = ReportHistory(project_id=json_data["project_id"],
                                   data=report_data,
                                   user_id=json_data["user_id"])
            report.report_audit_data = diffs

            session.add(report)
            session.commit()
            return make_response('Report History added.', 201)

        except Exception as e:
            abort(400, message="Error while adding record Report History. " + str(e))
