import models.chart_data_models as c_model

def generate_balance_pie_charts(row, chartType, chartTitle,
                            chartHeight, hTitle, vTitle, isStacked, columns, values):
    chart = c_model.ChartData(chartType)
    chart.init_options(chartTitle, chartHeight, hTitle, vTitle, isStacked)
    for column in columns:
        chart.init_column(column[0], column[1])
    for value in values:
        chart.add_row(value)

    if (len(chart.rows) > 0):
        row.add_cell({}, chart)
    else:
        row.add_cell({}, {}, "Ошибка построения графика")
    pass

    pass