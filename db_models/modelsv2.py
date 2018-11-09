from sqlalchemy import Boolean, Date, DateTime, Float, Integer, ForeignKey, \
    String, Text, Column, JSON, ARRAY, select, func, and_
from sqlalchemy.orm import column_property, object_session, remote, foreign, aliased, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
import random

Base = declarative_base()

import modules.db_model_transformer_module as db_transformer


# user table
class Log(Base):
    __tablename__ = 'log'
    id = Column('id', Integer, primary_key=True)
    date = Column('date', DateTime, default=datetime.datetime.utcnow())
    message = Column('message', Text)

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


# user table
class Users(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    first_name = Column('first_name', String(32))
    last_name = Column('last_name', String(32))
    lock_state = Column('lock_state', Boolean)
    client_id = Column('client_id', ForeignKey('clients.id'))
    user_role_id = Column('user_role_id', ForeignKey('user_roles.id'))

    login_data = relationship("UserLogins", backref="user_data", cascade="all,delete-orphan")
    user_project_data = relationship("Projects", backref="user_data", cascade="all,delete-orphan")
    user_documents_data = relationship("Documents", backref="user_data", cascade="all,delete-orphan")
    analytic_rules_data = relationship("AnalyticRules", backref="user_data", cascade="all,delete-orphan")
    chat_data = relationship("Chats", backref="user_data", cascade="all,delete-orphan")
    chat_message_data = relationship("ChatMessages", backref="user_data", cascade="all,delete-orphan")
    attachments_data = relationship("ProjectAttachments", backref="user_data", cascade="all,delete-orphan")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


# user roles
class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    users = relationship("Users", backref="user_role")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


# user logins
class UserLogins(Base):
    __tablename__ = 'user_logins'
    id = Column('id', Integer, primary_key=True)
    login = Column('login', String)
    password = Column('password', String)
    token = Column('token', String)
    registration_date = Column('registration_date', DateTime, default=datetime.datetime.utcnow())
    last_login_date = Column('last_login_date', DateTime, nullable=True)
    user_id = Column('user_id', ForeignKey('users.id'))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


# client type
class ClientTypes(Base):
    __tablename__ = 'client_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    clients = relationship("Clients", backref="client_type")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


# clients
class Clients(Base):
    __tablename__ = 'clients'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(70))
    registration_date = Column('registration_date', DateTime, default=datetime.datetime.utcnow())
    registration_number = Column('registration_number', String(25))
    lock_state = Column('lock_state', Boolean)
    client_type_id = Column('client_type_id', ForeignKey('client_types.id'))
    user_client = relationship("Users", backref="client")
    analytic_rules_data = relationship("AnalyticRules", backref="client_data")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


# user roles
class ProjectStates(Base):
    __tablename__ = 'project_states'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    states = relationship("Projects", backref="project_state")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


class ProjectSharing(Base):
    __tablename__ = 'project_sharing'
    id = Column(Integer, primary_key=True)
    project_id = Column('project_id', ForeignKey('projects.id'))
    users_ids = Column(ARRAY(Integer))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(70))
    creation_date = Column(DateTime, default=datetime.datetime.utcnow())
    state_id = Column('state_id', ForeignKey('project_states.id'), default=1)
    user_id = Column('user_id', ForeignKey('users.id'))
    control_log_state_id = Column(Integer, default=1)

    control_log_data = relationship("ProjectControlLog", backref="project_data", cascade="all,delete-orphan")
    chat_data = relationship("Chats", backref="project_data", cascade="all,delete-orphan")
    sharing_data = relationship("ProjectSharing", backref="project_data", cascade="all,delete-orphan")
    documents_data = relationship("Documents", backref="project_data", cascade="all,delete-orphan")
    reports_data = relationship("Reports", backref="project_data", cascade="all,delete-orphan")
    report_forms_data = relationship("ReportForms", backref="project_data", cascade="all,delete-orphan")
    analysis_log_data = relationship("ProjectAnalysisLog", backref="project_data", cascade="all,delete-orphan")
    analysis_data = relationship("ProjectAnalysis", backref="project_data", cascade="all,delete-orphan")
    transfer_cells_params_data = relationship("TransferCellsParams", backref="project_data",
                                              cascade="all,delete-orphan")
    attachments_data = relationship("ProjectAttachments", backref="project_data", cascade="all,delete-orphan")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
        self.name = "Заявка " + str(datetime.datetime.utcnow())


# document states
class DocumentStates(Base):
    __tablename__ = 'document_states'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    users = relationship("Documents", backref="document_state")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


# documents
class Documents(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(256))
    file_path = Column(String(256))
    file_size = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow())
    data = Column(JSON)
    document_type_id = Column(Integer)
    account_number = Column(String(800))
    is_excluded = Column(Boolean)
    document_state_id = Column('document_state_id', ForeignKey('document_states.id'), default=1)
    account_number = Column(String(800))
    is_excluded = Column(Boolean, default=False)
    project_id = Column('project_id', ForeignKey('projects.id'))
    user_id = Column('user_id', ForeignKey('users.id'))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


# reports
class Reports(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))
    analytic_rule_id = Column('analytic_rule_id', ForeignKey('analytic_rules.id'))
    analytic_rules_data = relationship('AnalyticRules', backref=backref('reports_data', cascade='all,delete-orphan'))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)

# report history
class ReportHistory(Base):
    __tablename__ = 'report_history'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))
    user_id = Column('user_id', ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.datetime.utcnow())
    project_data = relationship('Projects', backref=backref('report_history_data', cascade='all,delete-orphan'))
    user_data = relationship('Users', backref=backref('report_history_data', cascade='all,delete-orphan'))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)

# report audit types
class ReportAuditTypes(Base):
    __tablename__ = 'report_audit_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), default="")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)

# report operations
class ReportOperations(Base):
    __tablename__ = 'report_operations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), default="")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)

# report audit types
class ReportAudit(Base):
    __tablename__ = 'report_audit'
    id = Column(Integer, primary_key=True)
    history_id = Column('history_id', ForeignKey('report_history.id'))
    type_id = Column('type_id', ForeignKey('report_audit_types.id'))
    operation_id = Column('operation_id', ForeignKey('report_operations.id'))
    is_system = Column(Boolean, default=False)
    uid = Column(String(8), default='')
    text = Column(String, default="")
    report_history_data = relationship('ReportHistory',
                                       backref=backref('report_audit_data', cascade='all,delete-orphan'))
    operation_data = relationship('ReportOperations',
                                       backref=backref('report_audit_data', cascade='all,delete-orphan'))
    type_data = relationship('ReportAuditTypes',
                                       backref=backref('report_audit_data', cascade='all,delete-orphan'))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


# report forms
class ReportForms(Base):
    __tablename__ = 'report_forms'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))
    element_number = Column(Integer)
    period = Column(DateTime)

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
        self.period = datetime.datetime.strptime(self.period, "%Y-%m-%d %H:%M:%S")


class ProjectAnalysisLog(Base):
    __tablename__ = 'project_analysis_log'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
    # def __init__(self, projectId, data):
    #     self.project_id = projectId
    #     self.data = data


class ProjectAnalysis(Base):
    __tablename__ = 'project_analysis'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
    # def __init__(self, projectId, data):
    #     self.project_id = projectId
    #     self.data = data


class DefaultAnalyticRules(Base):
    __tablename__ = 'default_analytic_rules'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
    # def __init__(self, data):
    #     self.data = data


class AnalyticRules(Base):
    __tablename__ = 'analytic_rules'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_default = Column(Boolean)
    user_id = Column('user_id', ForeignKey('users.id'))
    client_id = Column('client_id', ForeignKey('clients.id'))
    created_date = Column(DateTime, default=datetime.datetime.utcnow())
    data = Column(JSON)

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
    # def __init__(self, name, is_default, user_id, client_id, data):
    #     self.name = name
    #     self.is_default = is_default
    #     self.user_id = user_id
    #     self.client_id = client_id
    #     self.created_date = datetime.datetime.now()
    #     self.data = data


class ConsolidateDataParams(Base):
    __tablename__ = 'consolidate_data_params'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
    # def __init__(self, data):
    #     self.data = data


class ProjectControlLog(Base):
    __tablename__ = 'project_control_log'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
    # def __init__(self, projectId, data):
    #     self.project_id = projectId
    #     self.data = data


class TransferCellsParams(Base):
    __tablename__ = 'transfer_cells_params'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    project_id = Column('project_id', ForeignKey('projects.id'))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
    # def __init__(self, projectId, data):
    #     self.project_id = projectId
    #     self.data = data


class Chats(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    name = Column(String(70))
    user_ids = Column(ARRAY(Integer), default=[])
    creator_id = Column('creator_id', ForeignKey('users.id'))
    is_open = Column(Boolean, default=False)
    project_id = Column('project_id', ForeignKey('projects.id'))
    messages = relationship("ChatMessages", backref="chat_data", cascade="all,delete-orphan")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)


class ChatMessages(Base):
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True)
    content = Column(String(5000))
    users_read = Column(ARRAY(Integer))
    user_id = Column('user_id', ForeignKey('users.id'))
    chat_id = Column('chat_id', ForeignKey('chats.id'))
    type = Column(Integer, default=1)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow())

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
    # def __init__(self, content, user_id, chat_id, type=1, users_read=[]):
    #     self.content = content
    #     self.user_id = user_id
    #     self.chat_id = chat_id
    #     self.type = type
    #     self.users_read = users_read
    #     self.creation_date = datetime.datetime.now()


# project_attachment_types
class ProjectAttachmentTypes(Base):
    __tablename__ = 'project_attachment_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    system_name = Column(String(256))
    filename_extensions = Column(ARRAY(String))
    icon = Column(String(256))
    attachments = relationship("ProjectAttachments", backref="type_data")

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
    # def __init__(self, name, system_name, filename_extensions, icon):
    #     self.created_date = datetime.datetime.now()
    #     self.name = name
    #     self.system_name = system_name
    #     self.filename_extensions = filename_extensions
    #     self.icon = icon


# project_attachments
class ProjectAttachments(Base):
    __tablename__ = 'project_attachments'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(256))
    file_path = Column(String(256))
    file_size = Column(Float)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow())
    text = Column(String(5000), default="")
    user_ids = Column(ARRAY(Integer), default=[])
    is_removed = Column(Boolean, default=False)

    type_id = Column('type_id', ForeignKey('project_attachment_types.id'))
    project_id = Column('project_id', ForeignKey('projects.id'))
    user_id = Column('user_id', ForeignKey('users.id'))

    def __init__(self, *args):
        db_transformer.transform_constructor_params(self, args)
    # def __init__(self, project_id, user_id, file_name, file_path, file_size, type_id, text='', user_ids=[],
    #              is_removed=False):
    #     self.creation_date = datetime.datetime.now()
    #     self.user_id = user_id
    #     self.project_id = project_id
    #     self.file_name = file_name
    #     self.file_path = file_path
    #     self.file_size = file_size
    #     self.type_id = type_id
    #     self.text = text
    #     self.user_ids = user_ids
    #     self.is_removed = is_removed


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from settings import DB_URI

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
