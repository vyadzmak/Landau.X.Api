import json
import models.chart_data_models as c_d_m
import models.table_data_model as t_d_m
import models.analytic_form_model as a_f_m
import modules.static_chart_builder as s_c_b
from decimal import Decimal
from re import sub
import zlib
import base64
import copy

from db_models.models import Users, Clients, AnalyticRules, Projects
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
import result_models.res_model as r_m
from sqlalchemy import and_
import datetime
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode()  # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value  # Instance of bytes


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode()  # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value  # Instance of str


def check_if_formula(type_id):
    try:
        f_letter = str(type_id)[0]
        if (f_letter == '2'):
            n = int(type_id)
            if (n >= 250):
                return True
            t = 0

        if (f_letter == '3'):
            n = int(type_id)
            if (n >= 350):
                return True
            t = 0
        return False
        pass
    except:
        return False
        pass


def get_formula_elements(project_id, type_id, analysis_type):
    try:
        types = []
        project = session.query(Projects).filter(Projects.id == int(project_id)).first()
        if (project == None):
            return []

        user_id = project.user_id

        user_client = session.query(Users).filter(Users.id == user_id).first()

        if not user_client:
            return []
        client_id = user_client.client_id

        analytic_rules = session.query(AnalyticRules).filter(and_(
            AnalyticRules.client_id == client_id),
            AnalyticRules.is_default == True
        ).first()
        model = json.loads(analytic_rules.data)

        if (str(type_id).startswith('2') and str(analysis_type) == '1'):
            # build to OSV
            pass
        else:
            if (str(type_id).startswith('2')):
                formulas = model["opiu_rules"]["card_rules"]["cards_formulas"]["opiu_cards_formulas"]
                for f in formulas:
                    if (f["code"] == type_id):
                        for element in f["formula_elements"]:
                            types.append(element['code'])
                        et = 0
                y = 0
                pass

            if (str(type_id).startswith('3')):
                formulas = model["odds_rules"]["odds_formulas"]["odds_formulas"]
                for f in formulas:
                    if (f["code"] == type_id):
                        for element in f["formula_elements"]:
                            types.append(element['code'])
                        et = 0
                y = 0
                pass

        t = 0
        return types
        pass
    except Exception as e:
        return []


def convert_details_by_period(documents, month, year, type_id, analysis_type, project_id):
    try:
        result = ""
        headers = []
        result = []
        is_formula = check_if_formula(type_id)
        clear_table = []
        types = []
        if (is_formula == False):
            types.append(type_id)
        else:
            types = get_formula_elements(project_id, type_id, analysis_type)

        for d in documents:

            s_cmpstr = copy.deepcopy(d.data)
            bc = s_cmpstr.count("b'")

            s_cmpstr = s_cmpstr.replace("b'", "", 1)
            qc = s_cmpstr.count("'")

            s_cmpstr = s_cmpstr.replace("'", "")
            b_cmpstr = to_bytes(s_cmpstr)
            b_cmpstr = base64.b64decode(b_cmpstr)
            rr = to_str(zlib.decompress(b_cmpstr))
            f_cmpstr = rr
            # f_cmpstr = f_cmpstr.replace("'", "")
            rr = json.loads(f_cmpstr)
            try:
                itms = rr["rows"][0]["cells"][0]["tableData"]["items"]
                if (len(headers) == 0):
                    headers = rr["rows"][0]["cells"][0]["tableData"]["headers"]
                tb = []
                for tp in types:

                    tb = []
                    if (year != 999 and not str(year).startswith('777')):
                        tb = [t for t in itms if
                              (
                              str(t["month"]) == str(month) and str(t["year"]) == str(year) and str(t["typeId"]) == str(
                                  tp))]
                        if (len(tb) > 0):
                            result.append(tb)
                    elif (year==999):
                        tb = [t for t in itms if
                              (
                                  str(t["typeId"]) == str(
                                      tp))]

                        if (len(tb) > 0):
                            result.append(tb)

                    elif (str(year).startswith('777')==True):
                        _year = int(str(year).replace('777',''))
                        tb = [t for t in itms if
                              (str(t["year"]) == str(_year) and str(
                                      t["typeId"]) == str(
                                      tp))
                              ]
                        if (len(tb) > 0):
                            result.append(tb)


            # genearate form

            except Exception as e:
                t = 0

        for r in result:
            for t in r:
                clear_table.append(t)
        if (analysis_type!='1' and str(type_id).startswith('2')==False):
            for p in clear_table:
                p["period"] =  datetime.datetime.strptime(p["period"], '%d.%m.%Y').date()
            clear_table.sort(key=lambda x: x["period"], reverse=False)
        form = a_f_m.AForm()
        if (str(type_id).startswith('2') and str(analysis_type) == '1'):
            #################################################
            form.add_row("Графики")
            row = form.get_last_row()

            # генерируем круговые диаграммы
            column_names = [['string', 'Наименование'], ['number', 'Показатели']]
            c_values = [['account', 'periodTransactionsDebet', 'Обороты за период по дебету'],
                        ['account', 'periodTransactionsCredit', 'Обороты за период по кредиту']
                        ]

            for c in c_values:
                values = []

                for detail in clear_table:
                    f_val = detail[c[0]]  # (getattr(detail, c[0]))
                    res = Decimal(sub(r'[^\d.]', '', detail[c[1]]))
                    s_val = float(res)  # (getattr(detail, c[1]))

                    v = [f_val, s_val]
                    values.append(v)
                all_nulls = True

                for v in values:
                    if (v[1] != 0):
                        all_nulls = False
                        break
                if (all_nulls):
                    continue
                s_c_b.generate_balance_pie_charts(row, 'PieChart',
                                                  c[2],
                                                  400,
                                                  c[2], "", False, column_names, values)


                ##############################
                #################################################
        form.add_row("Данные")
        table = t_d_m.TableData()
        table.headers = headers

        table.init_model(clear_table)
        # if (len(table.items)==0):
        #     #check is formula
        #     build_formula_details(table,rr)

        row = form.get_last_row()
        row.add_cell(table)

        return form
    except Exception as e:

        return ""
