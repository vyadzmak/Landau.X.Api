from db_models.modelsv2 import AnalyticRules
from flask_restful import Resource, fields
import json
from resv2.analytic_rules_resources import OUTPUT_FIELDS

# PARAMS
NAME = "SimpleAnalyticRulesResource"
NAME_LIST = "SimpleAnalyticRulesListResource"
ENTITY_NAME = "SimpleAnalyticRulesResource"
MODEL = AnalyticRules
ROUTE = "/v2/simpleAnalyticsRules"
END_POINT = "v2-simple-analytics-rules"
ROUTE_LIST = ROUTE+"List"
END_POINT_LIST = END_POINT + "-list"


# NESTED SCHEMA FIELDS
# OUTPUT FIELDS

def put_data_converter(json_data):
    json_data = json.loads(json_data)
    json_data = json.dumps(json_data, ensure_ascii=False)

    return {'data': json_data}


def post_data_converter(json_data):
    result = put_data_converter(json_data)
    result['name'] = "Правила для Казахстана"
    result['is_default'] = True
    result['client_id'] = 2
    result['user_id'] = 1
    return result
