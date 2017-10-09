class Transaction():

    #init
    def __init__(self, date, document, analyticDebet, analyticCredit,accountDebet, accountCredit, valueDebet, valueCredit):
        try:
            # if (self.check_date(date)):
                document= document
                analyticCredit = analyticCredit
                analyticDebet = analyticDebet

                self.period = date

                self.document = document
                self.analyticsDebet =analyticDebet
                self.analyticsCredit =analyticCredit
                self.accountDebet = accountDebet
                self.accountCredit =accountCredit
                self.valueDebet =valueDebet
                self.valueCredit =valueCredit
                self.processed = False
                self.valueCreditMinusDebet = ""
                self.valueDebetMinusCredit = ""
                self.dataType = -1
                self.style =""

        except:
            pass