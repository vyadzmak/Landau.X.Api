from flask import Flask
from flask_restful import Resource, Api
from json_encoder import AlchemyEncoder
from flask_cors import CORS

# init application
app = Flask(__name__)

# cors = CORS(app, resources={r"/login/*": {"origins": "*"}})
CORS(app, expose_headers=["Access-Token", "Uid", "Content-Disposition"])
# , allow_headers =["Access-Control-Expose-Headers"],
#
app.config['BUNDLE_ERRORS'] = True
json_encoder = AlchemyEncoder
app.json_encoder = json_encoder
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
api = Api(app)
# import resources
from res.user_roles_resources import *
from res.client_types_resources import *
from res.clients_resources import *
from res.users_resources import *
from res.user_logins_resources import *
from res.log_resources import *
from res.upload_resources import *
from res.projects_resources import *
from res.documents_resources import *
from res.reports_resources import *
from res.details_resources import *
from res.reports_forms_resources import *
from res.project_analysis_log_resources import *
from res.project_analysis_resources import *
from res.default_analytic_rules_resources import *
from res.analytic_rules_resources import *
from res.project_control_log_resources import *
from res.project_sharing_resources import *
from res.export_resources import *
from res.import_resources import *
from res.consolidate_data_resources import *
from res.transfer_cells_resources import *
from res.analytic_rule_elements_resource import *
from res.ssl_confirmation_resource import *
from res.chats_resources import *
from res.chat_messages_resources import *

# add resources
# user roles
api.add_resource(UserRoleListResource, '/userRoles', endpoint='user-roles')
api.add_resource(UserRoleResource, '/userRole/<int:id>', endpoint='user-role')

# client types
api.add_resource(ClientTypeListResource, '/clientTypes', endpoint='client-types')
api.add_resource(ClientTypeResource, '/clientType/<int:id>', endpoint='client-type')

# clients
api.add_resource(ClientListResource, '/clients', endpoint='clients')
api.add_resource(ClientResource, '/client/<int:id>', endpoint='client')

# users
api.add_resource(ClientUsersListResource, '/clientUsers/<int:id>', endpoint='client-users')
api.add_resource(UserListResource, '/users', endpoint='users')
api.add_resource(UserResource, '/user/<int:id>', endpoint='user')

# user logins
api.add_resource(UserLoginListResource, '/userLogins', endpoint='usersLogins')
api.add_resource(UserLoginResource, '/userLogin/<int:id>', endpoint='userLogin')
api.add_resource(UserAuthResource, '/login', endpoint='login')

# log
api.add_resource(LogListResource, '/log', endpoint='log')

# upload files
api.add_resource(UploadFile, '/upload', endpoint='upload')

# projects
api.add_resource(UserProjectList, '/userProjects/<int:id>', endpoint='userProjects')
api.add_resource(ProjectListResource, '/projects', endpoint='projects')
api.add_resource(ProjectResource, '/project/<int:id>', endpoint='project')

# documents
api.add_resource(ProjectDocumentListResource, '/projectDocuments/<int:id>', endpoint='projectDocuments')
api.add_resource(DocumentListResource, '/documents', endpoint='documents')
api.add_resource(BatchDocumentListResource, '/batchDocuments', endpoint='batchDocuments')
api.add_resource(DocumentResource, '/document/<int:id>', endpoint='document')

# reports
api.add_resource(ProjectReportResource, '/projectReport/<int:id>', endpoint='projectReport')
api.add_resource(ReportListResource, '/reports', endpoint='reports')
api.add_resource(ReportResource, '/report/<int:id>', endpoint='report')

# cell details
api.add_resource(CellDetailsListResource, '/cellDetails', endpoint='cellDetails')

# report forms
api.add_resource(ReportFormsListResource, '/reportForms', endpoint='reportForms')

# project analysis log
api.add_resource(ProjectSelectAnalysisLogResource, '/projectSelectAnalysisLog/<int:id>',
                 endpoint='projectSelectAnalysisLog')
api.add_resource(ProjectAnalysisLogResource, '/projectAnalysisLog/<int:id>', endpoint='projectAnalysisLog')
api.add_resource(ProjectAnalysisLogListResource, '/projectAnalysisLogs', endpoint='projectsAnalysisLog')

# project analysis data
api.add_resource(ProjectSelectAnalysisResource, '/projectSelectAnalysis/<int:id>', endpoint='projectSelectAnalysis')
api.add_resource(ProjectAnalysisResource, '/projectAnalysis/<int:id>', endpoint='projectAnalysis')
api.add_resource(ProjectAnalysisListResource, '/projectAnalysis', endpoint='projectsAnalysis')
api.add_resource(ProjectAnalysisRemover, '/projectCleanData/<int:id>', endpoint='projectCleanData')

# default analytic rules
api.add_resource(SimpleDefaultAnalyticRulesResource, '/simpleDefaultAnalyticsRules/<int:id>',
                 endpoint='simpleDefaultAnalyticRules')
api.add_resource(DefaultAnalyticRulesResource, '/defaultAnalyticsRules/<int:id>', endpoint='defaultAnalyticRules')
api.add_resource(DefaultAnalyticRulesListResource, '/defaultAnalyticsRules', endpoint='defaultAnalyticsRules')

# default analytic rules
api.add_resource(SimpleAnalyticRulesResource, '/simpleAnalyticsRules/<int:id>', endpoint='simpleAnalyticRules')
api.add_resource(SimpleAnalyticRulesListResource, '/simpleAnalyticsRulesList', endpoint='simpleAnalyticRulesList')
api.add_resource(AnalyticRulesResource, '/analyticsRules/<int:id>', endpoint='analyticRules')
api.add_resource(AnalyticRulesListResource, '/analyticsRules', endpoint='analyticsRules')

api.add_resource(ClientAnalyticRulesDefaultResource, '/analyticsRulesDefault/<int:id>', endpoint='analyticRulesDefault')
api.add_resource(ClientAnalyticRulesList, '/analyticsRulesClient/<int:id>', endpoint='analyticRulesClient')
api.add_resource(UserClientAnalyticRulesDefaultResource, '/analyticsRulesUserClient/<int:id>',
                 endpoint='analyticsRulesUserClient')

# control log
api.add_resource(ProjectSelectControlLogResource, '/projectSelectControlLog/<int:id>',
                 endpoint='projectSelectControlLog')
api.add_resource(ProjectControlLogResource, '/projectControlLog/<int:id>', endpoint='projectControlLog')
api.add_resource(ProjectControlLogListResource, '/projectControlLog', endpoint='projectsControlLog')

# project_sharing
api.add_resource(ProjectSharingListResource, '/projectSharings', endpoint='projectSharings')
api.add_resource(ProjectSharingResource, '/projectSharing/<int:id>', endpoint='projectSharing')

# export analytic rules
api.add_resource(ExportDefaultAnalyticRulesResource, '/exportDefaultSchema', endpoint='exportDefaultSchema')
api.add_resource(ExportAnalyticRulesResource, '/exportSchema/<int:id>', endpoint='exportSchema')

# import analytic rules
api.add_resource(ImportDefaultAnalyticRulesResource, '/importDefaultSchema', endpoint='importDefaultSchema')
api.add_resource(ImportAnalyticRulesResource, '/importSchema', endpoint='importSchema')
api.add_resource(ExportProjectsResource, '/exportProject/<int:id>', endpoint='exportProject')

# consolidation
api.add_resource(ConsolidateDataResource, '/consolidateDataParams/<int:id>', endpoint='consolidateDataParam')
api.add_resource(ConsolidateDataListResource, '/consolidateDataParams', endpoint='consolidateDataParams')
api.add_resource(MakeConsolidateResource, '/makeConsolidateData', endpoint='makeConsolidateData')

# transfer cells
api.add_resource(TransferCellsResource, '/transferCells/<int:id>', endpoint='transferCell')
api.add_resource(TransferCellsListResource, '/transferCells', endpoint='transferCells')
api.add_resource(MakeTransferCellsResource, '/makeTransferCells', endpoint='makeTransferCells')

# analytic rule elements
api.add_resource(AnalyticRuleElementsResource, '/getAnalyticRuleElements', endpoint='analyticRuleElements')

# chats
api.add_resource(ChatListResource, '/chats', endpoint='chats')
api.add_resource(ChatResource, '/chats/<int:id>', endpoint='chat')

# chat_messages
api.add_resource(ChatMessageListResource, '/chatMessages', endpoint='chatMessages')
api.add_resource(ChatMessageResource, '/chatMessages/<int:id>', endpoint='chatMessage')
api.add_resource(ChatMessageUnreadResource, '/unreadMessages', endpoint='unreadMessages')

api.add_resource(SSLConfirmationResource, '/.well-known/acme-challenge/<path:file>', endpoint='SSL-confirmation')

api.add_resource(ExportSingleDocumentResource, '/exportSingleDocument/<int:id>', endpoint='exportSingleDocument')
api.add_resource(ExportDocumentsResource, '/exportDocuments/<int:id>', endpoint='exportDocuments')

# start application
if __name__ == '__main__':
    # u_s.get_user_roles()
    # , ssl_context = 'adhoc'
    app.run(debug=True)
