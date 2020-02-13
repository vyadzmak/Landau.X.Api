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
            self.value_cell_column_index = 'AH'
            self.date_cell_column_index = 'W'

            # счета к получению
            self.accounts_receivable_arr = [[15, 104, 6]]

            # Предоплата поставщикам
            self.prepayment_to_suppliers_arr = [[23, 105, 6]]

            # Товар в пути
            self.goods_in_transit_arr = [[31, 106, 6]]

            # счета  к оплате
            self.invoices_for_payment_arr = [[41, 118, 6]]

            # Товарный кредит
            self.commodity_loan_arr = [[49, 119, 6]]

            # Предоплата клиентами
            self.customer_prepayment_arr = [[57, 120, 6]]

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
                    date_cell_index = self.date_cell_column_index + str(i)
                    value_cell_index = self.value_cell_column_index + str(i)

                    static_cell = StaticNameValueDateCell(name_cell_index, value_cell_index, date_cell_index,
                                                          rule_index,
                                                          self.sheet)

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
