from models.static_data_documents_models.general_models import StaticDateCell
from dateutil.parser import parse
from datetime import date
class OpiuStaticDocument():
    def __init__(self,file_path,file_name,  sheet):
        try:
            self.file_path = file_path
            self.file_name = file_name
            self.sheet = sheet
            self.day_cell_index = 'W10'
            self.month_cell_index = 'Z10'
            self.year_cell_index = 'AC10'
            self.document_date = None
            self.date_cell_column_indexes = ['V12','AB12','AG12']
            self.value_dates = []
            self.columns = []
            #1. ВЫРУЧКА ОТ РЕАЛИЗАЦИИ
            self.revenue_from_sales_arr = [[13,200]]

            #СТОИМОСТЬ ТОВАРОВ
            self.cost_of_goods_arr = [[17,207]]

            #зарплата
            self.salary_arr = [[23,208]]

            #аренда помещений
            self.rental_arr = [[24,209]]

            # коммунальные платежи
            self.communal_payments_arr = [[25,209]]

            #Транспортные и командировочные расходы
            self.travel_expenses_arr = [[26,210]]

            #Налоги
            self.taxes_arr = [[27,215]]

            #  Проценты по кредитам сторонних банков
            self.third_party_banks_interest_loans_arr = [[28,216]]

            # Проценты по  текущему кредиту в Банка ВТБ(ПАО)
            self.vtb_bank_interst_loans_arr = [[29,216]]

            # Прочие расходы (охрана, связь, авансовые расходы и т.д.)
            self.other_administrative_expenses_arr = [[30,213]]

            # 6. Другие доходы
            self.other_incomes_arr = [[32,218]]

            # расходы на семью
            self.family_expenses_arr = [[33,219]]

            # Прочие расходы (охрана, связь, авансовые расходы и т.д.)
            self.other_expenses_arr = [[34,219]]


            #10. Погашение основного долга по кредитам сторонних банков
            self.repayment_of_principal_on_loans_to_other_banks_arr=[[36,216]]

            # 11. Погашение основного долга по кредитам Банка ВТБ
            self.repayment_of_principal_on_vtb_bank_loans_arr = [[37,216]]

            self.parse_document_date()
            self.parse_value_dates()
            self.parse_values()
            self.sheet = None
            pass
        except Exception as e:
            pass

    #parse document date
    def parse_document_date(self):
        try:
            day_value = self.sheet[self.day_cell_index].value
            month_value = self.sheet[self.month_cell_index].value
            year_value = self.sheet[self.year_cell_index].value

            self.document_date = date(year_value,month_value,day_value)
            t=0
        except Exception as e:
            pass

    def parse_value_dates(self):
        try:
            for date_cell in self.date_cell_column_indexes:
                cell = self.sheet[date_cell]
                self.columns.append(cell.column_letter)
                self.value_dates.append(cell.value)
                t=0

            t=0
            pass
        except Exception as e:
            pass

    def parse_values(self):
        try:
            column_index =0
            all_attributes = dir(self)
            target_attributes = []
            for attribute in all_attributes:
                if (str(attribute).endswith('_arr')):
                    target_attributes.append(str(attribute))
            for column in self.columns:
                for attribute in target_attributes:
                    o = getattr(self,attribute)
                    row_index = o[0][0]
                    rule_index = o[0][1]
                    cell_index = column+str(row_index)
                    static_cell  =StaticDateCell(cell_index,rule_index,self.value_dates[column_index],
                                   self.sheet)
                    o.append(static_cell)
                column_index+=1

            for attribute in target_attributes:
                o = getattr(self,attribute)
                del o[0]
            t=0
            pass
        except Exception as e:
            pass

