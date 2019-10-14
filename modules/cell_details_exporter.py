from db_models.models import DefaultAnalyticRules, AnalyticRules, Reports, Projects, Documents
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import desc
from flask import Flask, make_response, send_from_directory, send_file
from flask import Response
import urllib.parse as urllib
from decimal import Decimal
from re import sub
import modules.export_document_formatter as formatter
import xlsxwriter
import json
from settings import EXPORT_FOLDER
import os
import uuid
import unicodedata
import string
from transliterate import translit, get_available_language_codes

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
import datetime
import zlib
import base64
import copy
import json
import zipfile
import shutil


def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    filename = filename.replace('(', '')
    filename = filename.replace(')', '')
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    return ''.join(c for c in cleaned_filename if c in whitelist)


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



def export_cells(worksheet, data, workbook):
    try:
        # row, col, value
        row_index = 0
        cell_index = 0
        header = None
        none_headers = []
        if (len(data)>0):
            _header =data[0]
            if (len(_header)>0):
                header = _header[0]
            index=0
            for header_item in header:
                if (header_item=='' or str(header_item).startswith('Обороты за ') or str(header_item).startswith('Сальдо на ') ):
                    none_headers.append(index)

                index+=1
        for row in data:

            for cell_line in row:
                row_index += 1
                cell_index = 0
                for cell in cell_line:
                        cell_index += 1

                        value = cell
                        _format = None
                        _cell_index =cell_index-1
                        exists = _cell_index in none_headers
                        if (exists==True and value!=''):

                            try:
                                ex = ',' in  str(value)
                                if (ex==True):
                                    value = str(value).replace(',', '')
                                # s_value = str(value).replace(',','')
                                # s_value = str(s_value).replace('.',',')
                                value = float(value)
                                pass
                            except Exception as e:
                                t=0
                                pass

                            _format = workbook.add_format()
                            _format.set_align('center')
                            _format.set_align('vcenter')
                            _format.set_num_format('#,##0.00')

                        if (_format != None):
                            worksheet.write(row_index - 1, cell_index - 1, value, _format)
                        else:
                            worksheet.write(row_index - 1, cell_index - 1, value)
    except Exception as e:
        pass



def convert_report(data,is_report):
    try:
        row_index =0

        if (is_report==True):
            row_index=1


            rows = data["rows"][row_index]["cells"][0]["tableData"]["items"]
            headers = data["rows"][row_index]["cells"][0]["tableData"]["headers"]

        else:
            rows = data.rows[0].cells[0].tableData.items
            headers = data.rows[0].cells[0].tableData.headers
        tt = 0
        titles = []
        names = []

        for header in headers:
            titles.append(header["text"])
            if (header["value"]!='indicators'):
                names.append(header["value"])

        index =0
        r_index =-1
        for title in titles:
            if (title=='*' and index==0):
                titles[index] ='Наименование'

            if (title == '*' and index > 0):
                r_index=index
                break

            index+=1
        if (r_index!=-1):
            titles.remove(titles[r_index])

        export_rows = []

        for row in rows:
            _row = []
            for name in names:
                if (name in row):
                    value = row[name]

                    if (name=='valueDebet' or name=='valueCredit'):
                        # pass
                        value = value.replace(',','')
                        # value = value.replace('.',',')

                    _row.append(value)

            export_rows.append(_row)
        result_rows = []

        result_rows.append([titles])
        result_rows.append(export_rows)
        t = 0
        return names,result_rows
    except Exception as e:
        return None


def export_cell_details(_data, is_report):
    try:
        if (is_report==True):
            data = json.loads(_data)
        else:
            data = _data


        names,converted_data_rows= convert_report(data,is_report)

        t=0
        dir_id = str(uuid.uuid4().hex)
        project_folder = os.path.join(EXPORT_FOLDER, dir_id)
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)

        project_name = "export_cell_details_"
        project_name = translit(project_name, 'ru', reversed=True)

        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt = str(dt).replace('-', '')
        project_name = project_name + "_" + str(dt)

        file_name = clean_filename(project_name)
        file_name = file_name.replace('__', "_")
        file_path = os.path.join(project_folder, file_name + ".xlsx")

        if (len(file_path) > 255):
            file_path = os.path.join(project_folder, dir_id + ".xlsx")

        workbook = xlsxwriter.Workbook(file_path)
        sheet_name = 'Landau Data'
        worksheet = workbook.add_worksheet(sheet_name)
        widths = formatter.get_column_widths(converted_data_rows)
        formatter.generate_worksheet_styles(workbook, worksheet, names)
        index = 0
        for width in widths:
            worksheet.set_column(index, index, width)
            index += 1

        export_cells(worksheet, converted_data_rows, workbook)
        workbook.close()
        return project_folder, file_name + ".xlsx"
        pass
    except Exception as e:
        pass