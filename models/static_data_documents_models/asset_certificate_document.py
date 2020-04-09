from models.static_data_documents_models.general_models import StaticNameValueDateCell
from dateutil.parser import parse
from datetime import date
from random import randint
class DebtCreditCertificateStaticDocument():
    def __init__(self,file_path,file_name,  sheet):
        try:
            self.id = randint(1,10000)
            self.file_path = file_path
            self.file_name = file_name
            self.sheet = sheet
            self.day_cell_index = 'W10'
            self.month_cell_index = 'Z10'
            self.year_cell_index = 'AC10'
            self.document_date = None

            self.name_cell_column_index = 'B'
            self.creditor_name_cell_column_index = 'F'
            self.credit_sum_cell_column_index = 'M'
            self.balance_credit_sum_cell_column_index = 'P'
            self.percent_credit_cell_column_index = 'S'
            self.date_credit_cell_column_index = 'U'

            # кредит
            self.credits_arr = [[15, 122, 3]]

            # лизинг
            self.leasing_arr = [[19, 122, 2]]

            # займ
            self.loan_arr = [[31,121, 1]]

            # факторинг
            self.factoring_arr = [[41, 123, 1]]

            self.parse_document_date()
            self.parse_values()
            self.sheet = None
            pass
        except Exception as e:
            pass

    # parse document date
    def parse_document_date(self):
        try:
            day_value = self.sheet[self.day_cell_index].value
            month_value = self.sheet[self.month_cell_index].value
            year_value = self.sheet[self.year_cell_index].value

            self.document_date = date(year_value, month_value, day_value)
            t = 0
        except Exception as e:
            pass

    def parse_values(self):
        try:
            column_index = 0
            all_attributes = dir(self)
            target_attributes = []
            for attribute in all_attributes:
                if (str(attribute).endswith('_arr')):
                    target_attributes.append(str(attribute))

            for attribute in target_attributes:
                o = getattr(self, attribute)
                row_index = o[0][0]
                rule_index = o[0][1]
                max_row = o[0][2]
                for i in range(row_index, row_index + max_row):
                    name_cell_index = self.name_cell_column_index + str(i)
                    creditor_cell_index = self.creditor_name_cell_column_index + str(i)
                    credit_sum_cell_index = self.credit_sum_cell_column_index + str(i)
                    balance_credit_sum_cell_index = self.balance_credit_sum_cell_column_index + str(i)
                    percent_credit_cell_index = self.percent_credit_cell_column_index + str(i)

                    static_cell =None# StaticNameValueDateCell(name_cell_index, value_cell_index, date_cell_index,
                                      #                    rule_index,
                                       #                   self.sheet)

                    if (static_cell.name != None):
                        if (static_cell.name == 'Прочие'):
                            if (static_cell.value > 0):
                                o.append(static_cell)
                        else:
                            o.append(static_cell)

            column_index += 1

            for attribute in target_attributes:
                o = getattr(self, attribute)
                del o[0]
            t = 0
            pass
        except Exception as e:
            t = 0
            pass
