from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, ForeignKey, String, Column, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

# user table
class Log(Base):
    __tablename__ = 'log'
    id = Column('id', Integer, primary_key=True)
    date = Column('date', DateTime)
    message = Column('message', String)

    def __init__(self, message):
        self.date = datetime.datetime.now()
        self.message = message


# user table
class Users(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    lock_state = Column('lock_state', Boolean)
    client_id = Column('client_id', ForeignKey('clients.id'))
    user_role_id = Column('user_role_id', ForeignKey('user_roles.id'))
    user_data = relationship("UserLogins", backref="user_data")
    user_project_data = relationship("Projects", backref="user_data")
    user_documents_data = relationship("Documents", backref="user_data")
    analytic_rules_data = relationship("AnalyticRules", backref="user_data")

    def __init__(self, first_name, last_name, lock_state, client_id, user_role_id):
        self.first_name = first_name
        self.last_name = last_name
        self.lock_state = lock_state
        self.client_id = client_id
        self.user_role_id = user_role_id


# user roles
class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    users = relationship("Users", backref="user_role")

    def __init__(self, name):
        self.name = name


# user logins
class UserLogins(Base):
    __tablename__ = 'user_logins'
    id = Column('id', Integer, primary_key=True)
    login = Column('login', String)
    password = Column('password', String)
    token = Column('token', String)
    registration_date = Column('registration_date', DateTime)
    last_login_date = Column('last_login_date', DateTime, nullable=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    user_login_data = relationship("Users", backref="login_data")

    def __init__(self,login,password,user_id):
        self.login = login
        self.password = password
        self.user_id = user_id
        self.registration_date = datetime.datetime.now()
    pass


# client type
class ClientTypes(Base):
    __tablename__ = 'client_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    clients = relationship("Clients", backref="client_type")


# clients
class Clients(Base):
    __tablename__ = 'clients'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(70))
    registration_date = Column('registration_date', DateTime)
    registration_number = Column('registration_number', String(25))
    lock_state = Column('lock_state', Boolean)
    client_type_id = Column('client_type_id', ForeignKey('client_types.id'))
    user_client = relationship("Users", backref="client")
    analytic_rules_data = relationship("AnalyticRules", backref="client_data")

    def __init__(self, name, registration_number, lock_state, client_type_id):
        self.name = name
        self.registration_number = registration_number
        self.lock_state = lock_state
        self.client_type_id = client_type_id
        self.registration_date = datetime.datetime.now()

# user roles
# user roles
class ProjectStates(Base):
    __tablename__ = 'project_states'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    states = relationship("Projects", backref="project_state")

    def __init__(self, name):
        self.name = name


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(70))
    creation_date = Column(DateTime)
    state_id = Column('state_id', ForeignKey('project_states.id'))
    user_id = Column('user_id', ForeignKey('users.id'))

    def __init__(self, userId):
        self.creation_date = datetime.datetime.now()
        self.name = "Заявка "+str(self.creation_date)
        self.state_id=1
        self.user_id =userId

#document states
class DocumentStates(Base):
    __tablename__ = 'document_states'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    users = relationship("Documents", backref="document_state")

    def __init__(self, name):
        self.name = name

#documents
class Documents(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(256))
    file_path = Column(String(256))
    file_size = Column(Float)
    created_date = Column(DateTime)
    data = Column(JSON)
    document_type_id = Column(Integer)
    document_state_id = Column('document_state_id',ForeignKey('document_states.id'))

    project_id = Column('project_id', ForeignKey('projects.id'))
    user_id = Column('user_id', ForeignKey('users.id'))

    def __init__(self,projectId, userId,file_name,file_path,file_size):
        self.created_date = datetime.datetime.now()
        self.user_id = userId
        self.project_id = projectId
        self.file_name = file_name
        self.file_path = file_path
        self.file_size = file_size
        self.document_state_id=1

#reports
class Reports(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))
    analytic_rule_id = Column('analytic_rule_id', ForeignKey('analytic_rules.id'))

    def __init__(self,projectId, name,data,analytic_rule_id):
        self.project_id = projectId
        self.name =name
        self.data= data
        self.analytic_rule_id = analytic_rule_id

#report forms
class ReportForms(Base):
    __tablename__ = 'report_forms'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))
    element_number =Column(Integer)
    period = Column(DateTime)
    def __init__(self,projectId,elementNumber,period, data):
        self.project_id = projectId
        self.element_number = elementNumber
        t =datetime.datetime.strptime(period, "%Y-%m-%d %H:%M:%S")
        self.period = t
        self.data = data

class ProjectAnalysisLog(Base):
    __tablename__ = 'project_analysis_log'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))
    def __init__(self,projectId, data):
        self.project_id = projectId
        self.data = data

class ProjectAnalysis(Base):
    __tablename__ = 'project_analysis'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))
    def __init__(self,projectId, data):
        self.project_id = projectId
        self.data = data

class DefaultAnalyticRules(Base):
    __tablename__ = 'default_analytic_rules'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)

    def __init__(self,data):
        self.data = data

class AnalyticRules(Base):
    __tablename__ = 'analytic_rules'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_default =Column(Boolean)
    user_id = Column('user_id', ForeignKey('users.id'))
    client_id = Column('client_id', ForeignKey('clients.id'))
    created_date = Column(DateTime)
    data = Column(JSON)


    def __init__(self,name,is_default, user_id,client_id,data):
        self.name =name
        self.is_default = is_default
        self.user_id = user_id
        self.client_id = client_id
        self.created_date = datetime.datetime.now()
        self.data = data


class ProjectControlLog(Base):
    __tablename__ = 'project_control_log'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))
    def __init__(self,projectId, data):
        self.project_id = projectId
        self.data = data

        
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from settings import DB_URI

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
