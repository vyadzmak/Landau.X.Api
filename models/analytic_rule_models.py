class AnalyticRule():
    def __init__(self,title, code,type):
        self.title = title
        self.code = code
        self.type = type



class AnalyticRules():
    def __init__(self):
        self.analytic_rules = []


    def add_analytic_rule(self,title,code,type):
        self.analytic_rules.append(AnalyticRule(title,code,type))