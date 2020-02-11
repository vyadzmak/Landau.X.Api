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

class StaticNameValueDateCell():
    def __init__(self,name_cell_index, value_cell_index, date_cell_index,system_rule_index,sheet):
        try:
            self.name_cell_index =name_cell_index
            self.value_cell_index =value_cell_index
            self.date_cell_index =date_cell_index
            self.value = self.get_value(sheet)
            self.name = self.get_name(sheet)
            self.date = self.get_date(sheet)
            self.system_rule_index = system_rule_index
        except Exception as e:
            pass

    def get_value(self,sheet):
        try:
            _value = sheet[self.value_cell_index].value
            if (_value==None or _value==''):
                _value = 0
            result =round(float(_value),2)
            return result
            pass
        except Exception as e:
            print('Error extract values in StaticNameValueDateCell {0}'.format(e))

    def get_name(self,sheet):
        try:
            result = sheet[self.name_cell_index].value
            return result
            pass
        except Exception as e:
            print('Error extract names in StaticNameValueDateCell {0}'.format(e))


    def get_date(self,sheet):
        try:
            result = sheet[self.date_cell_index].value
            return result
            pass
        except Exception as e:
            print('Error extract dates in StaticNameValueDateCell {0}'.format(e))