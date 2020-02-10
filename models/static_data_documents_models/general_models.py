class StaticDateCell():
    def __init__(self,  cell_index,system_rule_index,date,sheet):
        try:
            self.cell_index =cell_index
            self.value = self.get_value(sheet)
            self.date = date
            self.system_rule_index = system_rule_index
        except Exception as e:
            pass

    def get_value(self,sheet):
        try:
            _value = sheet[self.cell_index].value
            if (_value==None or _value==''):
                _value = 0
            result =round(float(_value),2)
            return result
            pass
        except Exception as e:
            print('Error extract values in StaticDateCell {0}'.format(e))