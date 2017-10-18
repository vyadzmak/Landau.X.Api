class ChartColumn():
    def __init__(self,type,label):
        self.type =type
        self.label = label
    pass

# class ChartRow():
#     def __init__(self):
#         pass
#
#     pass
class ChartAxis():
    def __init__(self, title, minValue="",maxValue=""):
        self.title= title
        self.minValue = minValue
        self.maxValue = maxValue


class ChartOptions():
    def __init__(self,title,height, hAxisTitle,vAxisTitle,isStacked):
        self.title =title
        self.hAxis = ChartAxis(hAxisTitle)
        self.vAxis = ChartAxis(vAxisTitle)
        self.height =height
        self.isStacked = isStacked
    pass


class ChartData():
    def __init__(self,chartType):
        self.chartType =chartType
        self.options ={}
        self.columns =[]
        self.rows = []
    pass

    #init options
    def init_options(self,title,height, hAxisTitle,vAxisTitle,isStacked):
        self.options = ChartOptions(title,height,hAxisTitle,vAxisTitle,isStacked)
        pass

    #init single column
    def init_column(self,type,label):
        self.columns.append(ChartColumn(type,label))

    #add row to chart
    def add_row(self,row):
        self.rows.append(row)



