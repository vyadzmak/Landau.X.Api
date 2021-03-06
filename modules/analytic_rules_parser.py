import json
import jsonpickle
import models.analytic_rule_models as a_r_model
from modules.json_serializator import engine_encode


def encode(ob):
    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)
        # jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        json_s = jsonpickle.encode(ob, unpicklable=False)
        return json_s
    except Exception as e:
        print(str(e))
        return ""


def parse_transaction_rules(conditions, analytic_rules):
    try:
        for condition in conditions:
            if (len(condition['document_account_masks'])==0 or len(condition['transaction_account_masks'])==0):
                continue
            code = condition['code']
            title = condition['name']
            type = condition['default_transaction_type']['type']['_value_']
            analytic_rules.add_analytic_rule(title, code, type)
            pass

    except Exception as e:
        pass


def parse_osv_rules(conditions, analytic_rules):
    try:
        for condition in conditions:
            if (len(condition['plus_account_masks'])==0 and len(condition['minus_account_masks'])==0):
                continue
            code = condition['code']
            title = condition['name']
            type = condition['default_account_type']['type']['_value_']
            analytic_rules.add_analytic_rule(title, code, type)

            pass

    except Exception as e:
        t=0
        pass


def parse_analytic_rules(sheet_id, data):
    try:
        rules = json.loads(data)
        analytic_rules = a_r_model.AnalyticRules()
        # получаем тип анализа
        analysis_type = rules["general_rules"]["general_rules_main"]["default_analysis_type"]["type"]["_value_"]

        if (analysis_type == 0):
            # cards
            # получаем данные в зависимости от sheet_id
            conditions = []
            if (sheet_id == 1):
                conditions = rules['balance_rules']['balance_conditions']['conditions']

            if (sheet_id == 2):
                # opiu_cards
                conditions = rules["opiu_rules"]["card_rules"]["cards_conditions"]["conditions"]

            elif (sheet_id == 3):
                # odds
                conditions = rules["odds_rules"]["odds_conditions"]["conditions"]
            if (sheet_id == 2 or sheet_id == 3):
                parse_transaction_rules(conditions, analytic_rules)
            elif (sheet_id == 1):
                parse_osv_rules(conditions, analytic_rules)
            pass
        elif (analysis_type == 1):
            # OSV
            pass

        return encode(analytic_rules)
        pass
    except Exception as e:
        return []
