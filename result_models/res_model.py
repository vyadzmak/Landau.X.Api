import datetime
import time
import locale
import math
import result_models.res_transaction as t
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


class TableModel():
    def __init__(self,headers, documents):
        try:
            self.headers = []
            for h in headers:
                self.headers.append(TableHeader(h["text"], h["value"]))

            self.footers = []
            self.items = []
            for document in documents:
                for transaction in document:
                        r = t.Transaction(
                            transaction["period"],
                            #date, document, analyticDebet, analyticCredit,accountDebet, accountCredit, valueDebet, valueCredit
                            transaction["document"],
                            transaction["analyticsDebet"],
                            transaction["analyticsCredit"],
                            transaction["accountDebet"],
                            transaction["accountCredit"],
                            transaction["valueDebet"],
                            transaction["valueCredit"]

                        )

                        # r.analyticsCredit = '\n'.split(str(e) for e in r.analyticsCredit)
                        # r.analyticsDebet = '\n'.join(str(e) for e in r.analyticsDebet)
                        # r.document = '\n'.join(str(e) for e in r.document)
                        #
                        # if (r.valueCredit == ""):
                        #     r.valueCredit = 0
                        # if (r.valueDebet == ""):
                        #     r.valueDebet = 0
                        #
                        # r.valueDebet = '{:0,.2f}'.format(round(r.valueDebet, 2))
                        # r.valueCredit = '{:0,.2f}'.format(round(r.valueCredit, 2))

                        r.style = "text-xs-center"
                        self.items.append(r)



        except Exception as e:
            print(str(e))


class FormModel():
    def __init__(self, headers,results):
        self.tableData = TableModel(headers,results)
        pass

