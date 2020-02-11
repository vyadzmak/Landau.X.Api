from models.static_data_documents_models.console_static_form_documents import ConsoleStaticFormDocuments
def process_documents(files):
    try:
        console_static_forms_documents = ConsoleStaticFormDocuments(files)
        return console_static_forms_documents
        pass
    except Exception as e:
        pass

