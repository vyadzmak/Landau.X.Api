import json
import models.chart_data_models as c_d_m
import models.table_data_model as t_d_m
import models.analytic_form_model as a_f_m
import modules.static_chart_builder as s_c_b
from decimal import Decimal
from re import sub
def convert_details_by_period(documents,month,year,type_id):
    try:
        result = ""
        headers = []
        result = []

        for d in documents:

            rr = json.loads(d.data)
            try:
                itms = rr["rows"][0]["cells"][0]["tableData"]["items"]

                if (len(headers) == 0):
                    headers = rr["rows"][0]["cells"][0]["tableData"]["headers"]
                tb = [t for t in itms if
                      (str(t["month"]) == month and str(t["year"]) == year and str(t["typeId"]) == str(type_id))]
                if (len(tb) > 0):
                    result.append(tb)

            #genearate form

            except Exception as e:
                t = 0

        clear_table = []
        for r in result:
            for t in r:
                clear_table.append(t)
        form = a_f_m.AForm()
        if (str(type_id).startswith('2')):
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
                    f_val = detail[c[0]]#(getattr(detail, c[0]))
                    res = Decimal(sub(r'[^\d.]', '',  detail[c[1]]))
                    s_val = float(res)#(getattr(detail, c[1]))

                    v = [f_val, s_val]
                    values.append(v)
                all_nulls =True

                for v in values:
                    if (v[1]!=0):
                        all_nulls =False
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
        row = form.get_last_row()
        row.add_cell(table)

        return form
    except Exception as e:

        return ""