class HeaderModel():
    def __init__(self,text,value):
        self.text = text
        self.value = value

class TableItem():
    def __init__(self):
        pass


class TableFooter():
    def __init__(self, text, style):
        self.text = text
        self.style = style
        pass


class TableHeader():
    def __init__(self, text, value, align="center", sortable=True):
        self.text = text
        self.align = align
        self.sortable = sortable
        if (len(value)>0):
            value = value[0].lower() + value[1:]
        self.value = value
        pass


class TableData():
    def __init__(self):
        self.headers = []
        self.footers = []
        self.items = []
        pass

    def init_headers(self,headers):
        for header in headers:
            self.headers.append(TableHeader(header.text, header.value))

    def init_model(self, lines):
        try:
            for line in lines:
                self.items.append(line)
        except Exception as e:
            print(str(e))






