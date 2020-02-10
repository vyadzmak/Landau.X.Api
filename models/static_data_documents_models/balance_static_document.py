from models.static_data_documents_models.general_models import StaticDateCell
from dateutil.parser import parse
class BalanceStaticDocument():
    def __init__(self, sheet):
        try:
            #шит документа
            self.sheet = sheet
            self.active_date_cell_index = 'F4'
            self.passive_date_cell_index = 'K4'

            #дата актива
            self.active_date = None

            #дата пассива
            self.passive_date = None

            self.parse_dates()
            #######ACTIVES######################################################################
            ####################################################################################
            #Касса
            self.cashbox = StaticDateCell('F6', 100, self.active_date, self.sheet)

            #Банковский счет
            self.bank_account = StaticDateCell('F7', 101, self.active_date, self.sheet)

            # Фин. вложения
            self.fin_investments = StaticDateCell('F8', 102, self.active_date, self.sheet)

            # Прочие краткоср.активы
            self.other_short_term_assets = StaticDateCell('F9', 103, self.active_date, self.sheet)

            #1. Всего ликвидных средств
            self.total_liquidity = StaticDateCell('F10', -1, self.active_date, self.sheet)

            # Счета к получению
            self.accounts_receivable =StaticDateCell('F12', 104, self.active_date, self.sheet)

            # Предоплата поставщикам
            self.prepayment_to_suppliers = StaticDateCell('F13', 105, self.active_date, self.sheet)

            # Товар в пути
            self.goods_in_transit = StaticDateCell('F14', 106, self.active_date, self.sheet)

            #2. Всего дебитор. задолж.
            self.total_receivables = StaticDateCell('F15', -1, self.active_date, self.sheet)

            # Итого сырье и п.ф.
            self.total_materials = StaticDateCell('F17', 107, self.active_date, self.sheet)

            #Итого готовая продукция
            self.total_products = StaticDateCell('F18', 108, self.active_date, self.sheet)

            # Итого товары
            self.total_goods =  StaticDateCell('F19', 109, self.active_date, self.sheet)

            # Итого ТМЗ
            self.total_inventory_costs = StaticDateCell('F20', -1, self.active_date, self.sheet)

            #Всего текущих активов
            self.total_current_assets = StaticDateCell('F22', -1, self.active_date, self.sheet)

            #Оборудование и мебель
            self.equipment_and_furniture = StaticDateCell('F24', 110, self.active_date, self.sheet)

            # Транспортные средства
            self.vehicles = StaticDateCell('F25', 111, self.active_date, self.sheet)

            # Недвижимость
            self.the_property = StaticDateCell('F26', 112, self.active_date, self.sheet)

            # Прочие постоянные активы активы
            self.other_fixed_assets = StaticDateCell('F27', 113, self.active_date, self.sheet)

            # Всего постоянных активов
            self.total_fixed_assets = StaticDateCell('F28', -1, self.active_date, self.sheet)

            # всего активы
            self.total_actives =  StaticDateCell('F30', -1, self.active_date, self.sheet)
            ####################################################################################

            #######PASSIVES######################################################################
            ####################################################################################

            # Расчеты с бюджетом
            self.settlements_with_the_budget = StaticDateCell('K6', 114, self.passive_date, self.sheet)

            #Задолженность по ЗП
            self.debt_payroll = StaticDateCell('K7', 115, self.passive_date, self.sheet)

            # Аренда и коммун.
            self.rent_and_utility_bills = StaticDateCell('K8', 116, self.passive_date, self.sheet)

            # Прочие краткоср.пассивы
            self.other_current_liabilities = StaticDateCell('K9', 117, self.passive_date, self.sheet)

            #7. Всего краткосрочная задолженность
            self.total_short_term_debt = StaticDateCell('K10', -1, self.passive_date, self.sheet)

            #Счета к оплате
            self.accounts_payable = StaticDateCell('K12', 118, self.passive_date, self.sheet)

            #Товарный кредит
            self.commodity_loan = StaticDateCell('K13', 119, self.passive_date, self.sheet)

            #Предоплата клиентами
            self.customer_prepayment = StaticDateCell('K14', 120, self.passive_date, self.sheet)

            #8. Всего среднесрочная задолженность
            self.total_medium_term_debt = StaticDateCell('K15', -1, self.passive_date, self.sheet)

            # Итого займы
            self.total_loans = StaticDateCell('K18', 121, self.passive_date, self.sheet)

            # Итого банковские кредиты
            self.total_bank_loans = StaticDateCell('K19', 122, self.passive_date, self.sheet)

            # 9. Всего краткосрочные кредиты
            self.total_short_term_loans = StaticDateCell('K20', -1, self.passive_date, self.sheet)

            # 10. Всего текущие задолженности
            self.total_current_debt = StaticDateCell('K22', -1, self.passive_date, self.sheet)

            # Долгосрочные кредиты
            self.long_term_loans = StaticDateCell('K24', 123, self.passive_date, self.sheet)

            # Прочие пассивы
            self.other_liabilities = StaticDateCell('K25', 124, self.passive_date, self.sheet)

            # 11. Всего долгосрочных обязательств
            self.total_long_term_liabilities = StaticDateCell('K26', -1, self.passive_date, self.sheet)

            # 12. Собственный капитал
            self.equity = StaticDateCell('K28', 125, self.passive_date, self.sheet)

            # всего пассивы
            self.total_passives = StaticDateCell('K30', -1, self.active_date, self.sheet)
            pass
        except Exception as e:
            pass

    #parse active and passive dates
    def parse_dates(self):
        try:
            self.active_date = str(self.sheet[self.active_date_cell_index].value.date())
            self.passive_date = str(self.sheet[self.passive_date_cell_index].value.date())

        except Exception as e:
            t=0
            pass

