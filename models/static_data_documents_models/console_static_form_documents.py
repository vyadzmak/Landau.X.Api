from openpyxl import load_workbook
from models.static_data_documents_models.balance_static_document import BalanceStaticDocument
class ConsoleStaticFormDocuments():
    def __init__(self,files):
        try:
            self.init_files(files)
            self.balance_static_document  =None
        except Exception as e:
            pass

    #init balance static document
    def init_balance_document_data(self,ws):
        try:
            self.balance_static_document = BalanceStaticDocument(ws)
            pass
        except Exception as e:
            pass

    #init opiu document data
    def init_opiu_document_data(self, ws):
        try:
            pass
        except Exception as e:
            pass



    def init_files(self,files):
        try:
            for file in files:
                wb = load_workbook(file['file_path'],read_only=True)
                ws = wb.worksheets[0]
                if (ws.title=='Resume_RUR'):
                    self.init_balance_document_data(ws)
                    self.init_opiu_document_data(ws)
                t=0

        except Exception as e:
            pass
