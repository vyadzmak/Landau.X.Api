from db_models.modelsv2 import DefaultAnalyticRules
from flask_restful import Resource, fields, marshal_with
from resv2.default_analytic_rules_resources import OUTPUT_FIELDS, put_data_converter
from modules.db_helper import update_item
from modules.log_helper_module import add_log
import json

class SimpleDefaultAnalyticRulesResource(Resource):
    def __init__(self):
        self.route = "/v2/simpleDefaultAnalyticsRules/<int:id>"
        self.end_point = "v2-simple-default-analytic-rules"
    @marshal_with(OUTPUT_FIELDS)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            json_data = put_data_converter(json_data)
            default_analytic_rules = update_item(DefaultAnalyticRules, json_data, id)
            return default_analytic_rules, 201
        except Exception as e:
            add_log("Exception on route: {0} - {1}".format(self.route, e))
            abort(400, "Error on route {}".format(self.route))