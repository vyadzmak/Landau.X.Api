class ExcludeTransactionsProjectDocument():
    def __init__(self):
        try:
            self.id = ''
            self.file_name = ''
            self.name =''

        except Exception as e:
            pass


class ConsolidationStaticDocument():
    def __init__(self):
        try:
            self.id = -1
            self.name = ''
            self.file_name = ''
        except Exception as e:
            pass


class AdditionalProjectDocuments():
    def __init__(self):
        try:
            self.exclude_transactions_document = []
            self.additional_consolidate_static_documents =[]
            pass
        except Exception as e:
            pass