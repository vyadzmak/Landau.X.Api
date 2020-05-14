
from db.db import session
from db_models.models import Formulars,AnalyticRules,Users,Clients
import datetime
class SchemaModel():
    def __init__(self):
        try:
            self.id = -1
            self.name = ''
            pass
        except Exception as e:
            pass

class FormularModel():
    def __init__(self):
        try:
            self.id = -1
            self.name = ''
            pass
        except Exception as e:
            pass

class ClientProduct():
    def __init__(self):
        try:
            self.id = -1
            self.client_id=-1
            self.name = ''
            self.formular_id =-1
            self.schema_id =-1
            self.creation_date =None
            self.user_id =-1
            self.schemas =[]
            self.formulars = []

        except Exception as e:
            pass

    def init_empty_model(self,user_id):
        try:
            self.user_id = user_id
            user = session.query(Users).filter(Users.id==user_id).first()
            self.client_id = user.client_id
            self.name = 'Product model '+str(datetime.datetime.now())

            _formulars = session.query(Formulars).filter(Formulars.client_id==self.client_id).all()
            _schemas = session.query(AnalyticRules).filter(AnalyticRules.client_id==self.client_id).all()

            for _formular in _formulars:
                formular = FormularModel()
                formular.id =_formular.id
                formular.name = _formular.file_name
                self.formulars.append(formular)

            for _schema in _schemas:
                schema = SchemaModel()
                schema.id = _schema.id
                schema.name = _schema.name
                self.schemas.append(schema)

            pass
        except Exception as e:
            pass