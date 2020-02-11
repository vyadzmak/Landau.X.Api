from openpyxl import load_workbook
from models.static_data_documents_models.balance_static_document import BalanceStaticDocument
from models.static_data_documents_models.opiu_static_document import OpiuStaticDocument
from models.static_data_documents_models.debt_credit_certificate_document import DebtCreditCertificateStaticDocument
class ConsoleStaticFormDocuments():
    def __init__(self,files):
        try:
            self.balance_static_document = None
            self.opiu_static_document = None
            self.deb_credit_certificate  = None
            self.has_error =False
            self.errors = []

            self.init_files(files)
        except Exception as e:
            pass

    #init balance static document
    def init_balance_document_data(self,file_path,file_name,ws):
        try:
            self.balance_static_document = BalanceStaticDocument(file_path,file_name,ws)

            pass
        except Exception as e:
            pass

    #init opiu document data
    def init_opiu_document_data(self,file_path,file_name, ws):
        try:
            self.opiu_static_document = OpiuStaticDocument(file_path,file_name,ws)
            pass
        except Exception as e:
            pass

        # init opiu document data
    def init_deb_credit_certificate_document_data(self,file_path,file_name, ws):
            try:
                self.deb_credit_certificate = DebtCreditCertificateStaticDocument(file_path,file_name,ws)
                pass
            except Exception as e:
                pass

    def init_files(self,files):
        try:
            for file in files:
                wb = load_workbook(file['file_path'],read_only=True)
                ws = wb.worksheets[0]
                if (ws.title=='Resume_RUR'):
                    self.init_balance_document_data(file['file_path'],file['file_name'],ws)

                if (ws.title=='Форма 1'):
                    self.init_opiu_document_data(file['file_path'],file['file_name'],ws)

                if (ws.title=='Форма 2'):
                    self.init_deb_credit_certificate_document_data(file['file_path'],file['file_name'],ws)

                t=0

        except Exception as e:
            pass
