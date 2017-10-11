import datetime
import time
import locale
import math
import result_models.res_transaction as t
import result_models.osv_transaction as o_t

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
    def __init__(self,headers, documents, doc_id):
        try:
            self.headers = []
            for h in headers:
                self.headers.append(TableHeader(h["text"], h["value"]))

            self.footers = []
            self.items = []
            if (doc_id==2):
                for document in documents:
                    for transaction in document:
                            r = o_t.Transaction(
                                transaction["account"],
                                #date, document, analyticDebet, analyticCredit,accountDebet, accountCredit, valueDebet, valueCredit
                                transaction["startPeriodBalanceDebet"],
                                transaction["startPeriodBalanceCredit"],
                                transaction["periodTransactionsDebet"],
                                transaction["periodTransactionsCredit"],
                                transaction["endPeriodBalanceDebet"],
                                transaction["endPeriodBalanceCredit"],


                            )


                            r.style = "text-xs-center"
                            self.items.append(r)
            elif (doc_id==1):
                for document in documents:
                    for transaction in document:
                        r = t.Transaction(
                            transaction["period"],
                            # date, document, analyticDebet, analyticCredit,accountDebet, accountCredit, valueDebet, valueCredit
                            transaction["document"],
                            transaction["analyticsDebet"],
                            transaction["analyticsCredit"],
                            transaction["accountDebet"],
                            transaction["accountCredit"],
                            transaction["valueDebet"],
                            transaction["valueCredit"]

                        )

                        r.style = "text-xs-center"
                        self.items.append(r)



        except Exception as e:
            print(str(e))


class FormModel():
    def __init__(self, headers,results,doc_id):
        self.tableData = TableModel(headers,results,doc_id)
        pass

