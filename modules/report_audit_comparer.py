from modules.json_serializator import decode, encode
from datetime import datetime
import traceback

letters_dict = {
    0: 'Z', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J',
    11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T',
    21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y'
}

engine_keys = {'analysis_type', 'analytical', 'analytical_type', 'document_type',
               'id', 'month', 'period', 'projectId', 'uid', 'year'}
unused_sheet_keys = {'arg', 'cal', 'lastVal', 'refs', 'value', 'timestamp'}
unused_keys = engine_keys | unused_sheet_keys


def get_letter_address(input):
    try:
        if input == 0:
            return ''
        a = input % 26
        b = input // 26
        result = letters_dict[a]
        if b == 0:
            return result
        else:
            if a == 0:
                return get_letter_address(b - 1) + result
            else:
                return get_letter_address(b) + result
    except Exception as e:
        print(e)
        return ''


def get_sheet_name(sheets, sheet_id):
    try:
        for sheet in sheets:
            if sheet['id'] == sheet_id:
                return sheet['name']
        return ''
    except Exception as e:
        print(e)
        return ''


def get_system_cell_text(json, document_type, analytical_type):
    try:
        if document_type == 1:
            period = json.get('period', False)
            if period:
                d = datetime.strptime(period, '%Y-%m-%d %H:%M:%S')
                period = " за период {}".format(datetime.strftime(d, '%d.%m.%Y'))

            else:
                period = ""
            return "(Баланс, {} {})".format(analytical_type, period)
        elif document_type == 2:
            month, year = json.get('month', ''), json.get('year', '')
            return "(ОПиУ, {} за период {}.{})".format(analytical_type, month, year)
        elif document_type == 3:
            month, year = json.get('month', ''), json.get('year', '')
            return "(ОДДС, {} за период {}.{})".format(analytical_type, month, year)
    except Exception as e:
        raise e


def get_cell_audit_type(key, data):
    try:
        if key == 'comment':
            return 4
        elif key == 'data':
            if str(data).startswith('='):
                return 3
            else:
                return 2
        else:
            return 5
    except Exception as e:
        print(e)
        return 1


def compare_json(json1, json2):
    try:
        result = []
        keys1 = set(json1.keys()) - unused_keys
        keys2 = set(json2.keys()) - unused_keys

        added_keys = keys2 - keys1
        deleted_keys = keys1 - keys2
        altered_keys = keys1.intersection(keys2)

        for key in added_keys:
            result.append({
                'text': 'Добавлено свойство {} со значением {}'.format(key, json2[key]),
                'operation_id': 1,
                'type_id': get_cell_audit_type(key, json2[key])
            })
        for key in deleted_keys:
            result.append({
                'text': 'Удалено свойство {}'.format(key),
                'operation_id': 3,
                'type_id': get_cell_audit_type(key, json1[key])
            })
        for key in altered_keys:
            if json1[key] != json2[key]:
                result.append({
                    'text': 'Изменено свойство {} с {} на {}'.format(key, json1[key], json2[key]),
                    'operation_id': 2,
                    'type_id': get_cell_audit_type(key, json2[key])
                })

        return result
    except Exception as e:
        print(e)
        return result


def get_diffs(prev_report, curr_report_data, rules):
    try:
        result = []
        prev_report_data = decode(prev_report)
        # comparing cells
        prev_cells = {x.get('json', {}).get('uid'): x for x in prev_report_data['cells']}
        curr_cells = {x.get('json', {}).get('uid'): x for x in curr_report_data['cells']}

        prev_keys = set(prev_cells.keys())
        curr_keys = set(curr_cells.keys())

        added_keys = curr_keys - prev_keys
        deleted_keys = prev_keys - curr_keys
        altered_keys = prev_keys.intersection(curr_keys)

        for key in added_keys:
            sheet_name = get_sheet_name(curr_report_data['sheets'], curr_cells[key]['sheet'])
            address = get_letter_address(curr_cells[key]['col']) + str(curr_cells[key]['row'])
            cell_data = curr_cells[key]['json'].get('data', '')
            text = "Данные на листе {} в ячейке {} - '{}'".format(sheet_name, address, cell_data)
            result.append({
                'operation_id': 1,
                'type_id': 1,
                'text': text,
                'is_system': False
            })

        for key in deleted_keys:
            sheet_name = get_sheet_name(prev_report_data['sheets'], prev_cells[key]['sheet'])
            address = get_letter_address(prev_cells[key]['col']) + str(prev_cells[key]['row'])
            analytical_type = int(prev_cells[key].get('json', {}).get('analytical_type', "") or 0)
            is_system = analytical_type > 0
            text = "Лист {} ячейка {}".format(sheet_name, address)
            if is_system:
                document_type = int(prev_cells[key].get('json', {}).get('document_type', "") or 0)
                text = "{} {}".format(text, get_system_cell_text(prev_cells[key].get('json', {}), document_type,
                                                               rules[str(analytical_type)]))
            result.append({
                'operation_id': 3,
                'type_id': 1,
                'text': text,
                'is_system': is_system
            })

        for key in altered_keys:
            if curr_cells[key].get('col', 0) == 0 and curr_cells[key].get('row', 0) == 0:
                continue
            cell_diffs = compare_json(prev_cells[key].get('json', {}), curr_cells[key].get('json', {}))
            for cell_diff in cell_diffs:
                sheet_name = get_sheet_name(curr_report_data['sheets'], curr_cells[key]['sheet'])
                address = get_letter_address(curr_cells[key]['col']) + str(curr_cells[key]['row'])
                analytical_type = int(curr_cells[key].get('json', {}).get('analytical_type', "") or 0)
                is_system = analytical_type > 0
                text = "Лист {} ячейка {} - {}".format(sheet_name, address, cell_diff['text'])
                if is_system:
                    document_type = int(curr_cells[key].get('json', {}).get('document_type', "") or 0)
                    text = "{} {}".format(text, get_system_cell_text(prev_cells[key].get('json', {}), document_type,
                                                                   rules[str(analytical_type)]))
                result.append({
                    'operation_id': cell_diff['operation_id'],
                    'type_id': cell_diff['type_id'],
                    'text': text,
                    'is_system': is_system
                })

        # comparing floatings
        prev_charts = {x.get('name', None): x for x in prev_report_data.get('floatings', [])
                       if x.get('ftype', '') == 'floor'}
        curr_charts = {x.get('name', None): x for x in curr_report_data.get('floatings', [])
                       if x.get('ftype', '') == 'floor'}

        prev_keys = set(prev_charts.keys())
        curr_keys = set(curr_charts.keys())

        added_keys = curr_keys - prev_keys
        deleted_keys = prev_keys - curr_keys
        altered_keys = prev_keys.intersection(curr_keys)

        for key in added_keys:
            sheet_name = get_sheet_name(curr_report_data['sheets'], curr_charts[key]['sheet'])
            chart_data = decode(curr_charts[key].get('json', "{}")).get('chartType')
            text = "На листе {} добавлен график".format(sheet_name)
            if chart_data is not None:
                text += ". Тип графика - {}".format(chart_data)
            result.append({
                'operation_id': 1,
                'type_id': 6,
                'text': text,
                'is_system': False
            })

        for key in deleted_keys:
            sheet_name = get_sheet_name(curr_report_data['sheets'], curr_charts[key]['sheet'])
            chart_data = decode(prev_charts[key].get('json', "{}")).get('chartType')
            text = "На листе {} удален график".format(sheet_name)
            if chart_data is not None:
                text += ". Тип графика - {}".format(chart_data)
            result.append({
                'operation_id': 3,
                'type_id': 6,
                'text': text,
                'is_system': False
            })

        for key in altered_keys:
            if curr_charts[key].get('json', '') != prev_charts[key].get('json', ''):
                sheet_name = get_sheet_name(curr_report_data['sheets'], curr_charts[key]['sheet'])
                chart_data = decode(curr_charts[key].get('json', "{}")).get('chartType')
                text = "На листе {} изменен график".format(sheet_name)
                if chart_data is not None:
                    text += ". Тип графика - {}".format(chart_data)
                result.append({
                    'operation_id': 2,
                    'type_id': 6,
                    'text': text,
                    'is_system': False
                })

        return result

    except Exception as e:
        print(traceback.format_exc())
