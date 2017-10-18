import models.table_data_model as t_d_m
import models.chart_data_models as c_d_m

#cell for anaytics
class ACell:
    def __init__(self,tableData={},chartData={},textData =""):
        self.tableData =tableData
        self.chartData = chartData
        self.textData =textData
        pass

#row for analytics
class ARow:
    #init row
    def __init__(self,title):
        self.title = title
        self.cells = []
        pass

    #add cell to current row
    def add_cell(self,tableData={},chartData={},textData =""):
        self.cells.append(ACell(tableData,chartData,textData))

#amalytics form
class AForm():
    #init Form
    def __init__(self):
        self.rows = []
        pass

    #add row to form
    def add_row(self,title):
        self.rows.append(ARow(title))
        pass

    def get_last_row(self):
        return self.rows[len(self.rows)-1]