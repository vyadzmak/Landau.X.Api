import os
import string
import unicodedata
import uuid

import xlsxwriter
from transliterate import translit

import modules.export_document_formatter as formatter
from settings import EXPORT_FOLDER

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
import datetime
import json


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
        is_osv = True
        none_headers = []
        if (len(data) > 0):
            _header = data[0]
            if (len(_header) > 0):
                header = _header[0]
            index = 0

            if (len(header) > 0):
                if (str(header[0]).startswith('Дата')):
                    is_osv = False

            for header_item in header:
                if (header_item == '' or str(header_item).startswith('Обороты за ') or str(header_item).startswith(
                        'Сальдо на ')):
                    none_headers.append(index)

                index += 1
        for row in data:

            for cell_line in row:
                row_index += 1
                cell_index = 0
                for cell in cell_line:
                    cell_index += 1

                    value = cell
                    _format = None
                    _cell_index = cell_index - 1
                    exists = _cell_index in none_headers
                    t = type(value)
                    is_numeric = False
                    is_int = t is int
                    is_float = t is float

                    if (is_int == True or is_float == True):
                        is_numeric = True

                    if ((exists == True and value != '') or is_numeric == True):

                        try:
                            ex = ',' in str(value)
                            if (ex == True):
                                value = str(value).replace(',', '')

                            value = float(value)
                            pass
                        except Exception as e:
                            t = 0
                            pass

                        _format = workbook.add_format()
                        _format.set_align('center')
                        _format.set_align('vcenter')
                        if (is_osv == True):
                            if (cell_index == 2):
                                _format.set_num_format('#,###')
                            else:
                                _format.set_num_format('#,##0.00')

                        else:
                            if (cell_index == 6 or cell_index == 8):
                                _format.set_num_format('#,###')
                            else:
                                _format.set_num_format('#,##0.00')

                    if (_format != None):
                        worksheet.write(row_index - 1, cell_index - 1, value, _format)
                    else:
                        worksheet.write(row_index - 1, cell_index - 1, value)
    except Exception as e:
        pass


def convert_report(data, is_report):
    try:
        row_index = 0

        if (is_report == True):
            row_index = 1

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
            if (header["value"] != 'indicators'):
                names.append(header["value"])

        index = 0
        r_index = -1
        for title in titles:
            if (title == '*' and index == 0):
                titles[index] = 'Наименование'

            if (title == '*' and index > 0):
                r_index = index
                break

            index += 1
        if (r_index != -1):
            titles.remove(titles[r_index])

        export_rows = []

        for row in rows:
            _row = []
            for name in names:
                if (name in row):
                    value = row[name]

                    if (name == 'valueDebet' or name == 'valueCredit'):
                        # pass
                        value = value.replace(',', '')
                        # value = value.replace('.',',')
                    elif (name == 'period'):
                        is_date_time = type(value) == datetime.datetime
                        is_date = type(value) == datetime.date
                        is_string = type(value) == str
                        if (is_date_time == True or is_date == True):
                            value = value.strftime("%d.%m.%Y")

                        t = 0
                    _row.append(value)

            export_rows.append(_row)
        result_rows = []

        result_rows.append([titles])
        result_rows.append(export_rows)
        t = 0
        return names, result_rows
    except Exception as e:
        return None


def export_cell_details(_data, is_report):
    try:
        if (is_report == True):
            data = json.loads(_data)
        else:
            data = _data

        names, converted_data_rows = convert_report(data, is_report)

        t = 0
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
