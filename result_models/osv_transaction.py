class Transaction():
    # init
    def __init__(self, account, startPeriodBalanceDebet, startPeriodBalanceCredit, periodTransactionsDebet,
                 periodTransactionsCredit, endPeriodBalanceDebet, endPeriodBalanceCredit):
        try:

            self.account = account

            self.endPeriodBalanceCredit = endPeriodBalanceCredit
            self.endPeriodBalanceDebet = endPeriodBalanceDebet
            self.startPeriodBalanceCredit = startPeriodBalanceCredit
            self.startPeriodBalanceDebet = startPeriodBalanceDebet
            self.periodTransactionsCredit = periodTransactionsCredit
            self.periodTransactionsDebet = periodTransactionsDebet
            self.processed = False

            self.dataType = -1
            self.style = ""

        except:
            pass
