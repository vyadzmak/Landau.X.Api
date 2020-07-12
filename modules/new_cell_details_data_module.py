from db_models.models import Documents,ReportForms
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
import result_models.res_model as r_m
from sqlalchemy import and_
import modules.details_converter as details_converter
import jsonpickle
import datetime
import copy
import base64
import zlib
import string
import models.analytic_form_model as a_f_m
import models.table_data_model as t_d_m
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode()  # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value  # Instance of bytes


def to_str(bytes_or_str):
    try:
        if isinstance(bytes_or_str, bytes):
                value = bytes_or_str.decode(encoding='utf-8')  # uses 'utf-8' for encoding
        else:
            value = bytes_or_str
        return value
    except Exception as e:
        print('TO STR ERROR '+str(e))


#extract data for  new cells
def extract_data(project_id, sheet_name, row_index, column_index):
    try:
        alphabet = list(string.ascii_uppercase)
        cell_index = alphabet[column_index] + str(row_index + 1)

        if (sheet_name=='Resume_RUR' or sheet_name=='Statyi balansa' or sheet_name=='Баланс'):
            report_forms = session.query(ReportForms).filter(and_(
                ReportForms.project_id == project_id,
            )

            ).all()

            for report_form in report_forms:
                data = json.loads(copy.deepcopy(report_form.data))

                if (data['additional_info']['cell_index']==cell_index and data['additional_info']['sheet_name']==sheet_name):

                    return report_form.data,False
                t=0


            return None




        documents = session.query(Documents).filter(
            Documents.project_id == project_id
        ).all()
        result_rows = []
        headers = []

        for d in documents:
            s_cmpstr = copy.deepcopy(d.data)

            s_cmpstr = s_cmpstr.replace("b'", "", 1)

            s_cmpstr = s_cmpstr.replace("'", "")
            b_cmpstr = to_bytes(s_cmpstr)
            b_cmpstr = base64.b64decode(b_cmpstr)

            tmp =None
            try:
                tmp = zlib.decompress(b_cmpstr)
            except Exception as e:
                pass

            if (tmp==None):
                continue
            del s_cmpstr
            del b_cmpstr

            rr = to_str(tmp)
            del tmp
            f_cmpstr = rr
            # f_cmpstr = f_cmpstr.replace("'", "")
            document_content = json.loads(f_cmpstr)
            items = document_content['rows'][0]['cells'][0]['tableData']['items']

            for item in items:
                if (item['cell_index']==cell_index and item['sheet_name']==sheet_name):
                    if (len(headers) == 0):
                        headers = document_content["rows"][0]["cells"][0]["tableData"]["headers"]
                    result_rows.append(item)

        clear_table = []

        for r in result_rows:
                clear_table.append(r)
        form = a_f_m.AForm()

        form.add_row("Данные")
        table = t_d_m.TableData()
        table.headers = headers

        table.init_model(clear_table)
        # if (len(table.items)==0):
        #     #check is formula
        #     build_formula_details(table,rr)

        row = form.get_last_row()
        row.add_cell(table)

        return form,True
        pass
    except Exception as e:
        return None,False