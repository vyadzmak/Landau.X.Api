from flask import Flask
from flask_restful import Resource, Api
from json_encoder import AlchemyEncoder
from flask_cors import CORS
import modules.resources_initializer as resources_initializer
from settings import dev_mode
from db.db import session
# init application
# app = Flask(__name__)
#
# # cors = CORS(app, resources={r"/login/*": {"origins": "*"}})
# CORS(app, expose_headers=["Access-Token", "Uid", "Content-Disposition"])
# # , allow_headers =["Access-Control-Expose-Headers"],
# #
# app.config['BUNDLE_ERRORS'] = True
# json_encoder = AlchemyEncoder
# app.json_encoder = json_encoder
# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024*16
# api = Api(app)

api = None

# import resources v1
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
from res.project_attachment_types_resources import *
from res.project_attachments_resources import *
from res.engine_resources import *
from res.report_history_resources import *
from res.report_audit_resources import *
from res.engine_pkb_resources import *
from res.export_cell_details_resources import *
from res.client_settings_resources import *
from res.export_original_documents_resources import *
from res.formular_versions_storage_resources import *
from res.console_static_documents_resources import *
from res.consolidate_mark_resources import *
from res.build_consolidate_excluded_rows_resources import *
from res.project_additional_documents_resources import *
from res.export_additional_documents_resources import *
from res.upload_formular_resources import *
from res.client_formulars_resources import *
from res.client_products_resources import *
from res.client_product_model_resources import *
from res.get_formular_resources import *

def init_api_resources(api):
    try:
        # add resources v1
        # user roles
        api.add_resource(UserRoleListResource, '/userRoles', endpoint='user-roles')
        api.add_resource(UserRoleResource, '/userRole/<int:id>', endpoint='user-role')

        # client types
        api.add_resource(ClientTypeListResource, '/clientTypes', endpoint='client-types')
        api.add_resource(ClientTypeResource, '/clientType/<int:id>', endpoint='client-type')

        # clients
        api.add_resource(ClientListResource, '/clients', endpoint='clients')
        api.add_resource(ClientResource, '/client/<int:id>', endpoint='client')
        api.add_resource(ClientSettingsResource, '/clientSettings/<int:id>', endpoint='client-settings')

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
        api.add_resource(UploadFormular, '/uploadFormular', endpoint='uploadFormular')

        # projects
        api.add_resource(UserProjectList, '/userProjects/<int:id>', endpoint='userProjects')
        api.add_resource(ProjectListResource, '/projects', endpoint='projects')
        api.add_resource(ProjectResource, '/project/<int:id>', endpoint='project')

        #consolidate marks
        api.add_resource(ConsolidateMarkListResource, '/consolidateMarks', endpoint='consolidateMarks')
        api.add_resource(ConsolidateMarkResource, '/consolidateMark/<int:id>', endpoint='consolidateMark')


        # documents
        api.add_resource(ProjectDocumentListResource, '/projectDocuments/<int:id>', endpoint='projectDocuments')
        api.add_resource(DocumentListResource, '/documents', endpoint='documents')
        api.add_resource(BatchDocumentListResource, '/batchDocuments', endpoint='batchDocuments')
        api.add_resource(DocumentResource, '/document/<int:id>', endpoint='document')
        api.add_resource(FullDocumentResource, '/fullDocument/<int:id>', endpoint='fullDocument')
        api.add_resource(ZipDocumentResource, '/zipDocument/<int:id>', endpoint='zipDocument')

        api.add_resource(ExcludeDocumentListResource, '/excludeDocuments', endpoint='excludeDocuments')
        api.add_resource(UploadAdditionalFile, '/uploadAdditional', endpoint='uploadAdditional')

        # reports
        api.add_resource(ProjectReportResource, '/projectReport/<int:id>', endpoint='projectReport')
        api.add_resource(ReportListResource, '/reports', endpoint='reports')
        api.add_resource(ReportResource, '/report/<int:id>', endpoint='report')

        # cell details
        api.add_resource(CellDetailsListResource, '/cellDetails', endpoint='cellDetails')
        api.add_resource(ExportCellDetailsListResource, '/exportCellDetails', endpoint='exportCellDetails')
        api.add_resource(NewCellDetailsListResource, '/newCellDetails', endpoint='newCellDetails')

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

        # project_attachments
        api.add_resource(ProjectAttachmentListResource, '/projectAttachments', endpoint='projectAttachments')
        api.add_resource(ProjectAttachmentResource, '/projectAttachments/<int:id>', endpoint='projectAttachment')
        api.add_resource(ExportProjectAttachmentResource, '/exportProjectAttachment/<int:id>', endpoint='exportProjectAttachment')

        # project_attachment_types
        api.add_resource(ProjectAttachmentTypeListResource, '/projectAttachmentTypes', endpoint='projectAttachmentTypes')
        api.add_resource(ProjectAttachmentTypeResource, '/projectAttachmentTypes/<int:id>', endpoint='projectAttachmentType')

        # engine
        api.add_resource(ProjectRecalculationResource, '/projectRecalculation', endpoint='projectRecalculation')

        # report history
        api.add_resource(ProjectReportHistoryListResource, '/projectReportHistoryList', endpoint='projectReportHistoryList')
        api.add_resource(ProjectReportHistoryResource, '/projectReportHistory/<int:id>', endpoint='projectReportHistory')
        api.add_resource(NewProjectReportHistoryResource, '/newProjectReportHistory/<int:id>', endpoint='newProjectReportHistory')
        api.add_resource(ReportHistoryListResource, '/reportHistoryList', endpoint='reportHistoryList')
        api.add_resource(ReportHistoryResource, '/reportHistory/<int:id>', endpoint='reportHistory')


        # export original documents
        api.add_resource(ExportOriginalDocumentsResource, '/exportOriginalDocuments/<int:id>', endpoint='exportOriginalDocuments')

        # formular versions storage
        api.add_resource(FormularVersionsStorageResources, '/formularVersionsStorage', endpoint='formularVersionsStorage')

        # console static documents
        api.add_resource(ConsoleStaticDocumentsResources, '/consoleStaticDocuments', endpoint='consoleStaticDocuments')
        api.add_resource(ConsoleStaticDocumentsResources, '/consoleStaticDocuments/<int:id>', endpoint='consoleStaticDocument')


        api.add_resource(ProjectAdditionalDocumentsResource, '/projectAdditionalDocuments/<int:id>', endpoint='projectAdditionalDocuments')


        api.add_resource(BuildConsolidateExcludedRowsDocumentsListResource, '/buildConsolidateExcludedRowsDocuments', endpoint='buildConsolidateExcludedRowsDocuments')


        # report audit
        api.add_resource(HistoryReportAuditListResource, '/historyReportAuditList', endpoint='historyReportAuditList')
        api.add_resource(CellReportAuditListResource, '/cellReportAuditList', endpoint='cellReportAuditList')

        # pkb report
        api.add_resource(EnginePkbResource, '/pkbReport', endpoint='pkbReport')

        # export additional documents
        api.add_resource(ExportStaticDocumentsResource, '/exportStaticDocuments', endpoint='exportStaticDocuments')
        api.add_resource(ExportExcludeTransactionsDocumentsResource, '/exportExcludeTransactionsDocuments/<int:id>', endpoint='exportExcludeTransactionsDocuments')

        api.add_resource(ClientFormularListResource, '/clientFormulars/<int:id>', endpoint='clientFormulars')
        api.add_resource(ClientProductsListResource, '/clientProducts/<int:id>', endpoint='clientProducts')
        api.add_resource(ClientProductsResource, '/clientProduct/<int:id>', endpoint='clientProduct')
        api.add_resource(ClientProductsListResource, '/clientProducts', endpoint='clientProductsR')
        api.add_resource(ClientProductModelResource, '/clientProductModel/<int:id>', endpoint='clientProductModel')
        api.add_resource(GetFormularResource, '/getFormular/<int:id>', endpoint='getFormular')

        # generate routes V2
        resources_initializer.init_api_resources(api)
    except Exception as e:
        pass

#create application
def create_app():
    try:
        app = Flask(__name__)
        app.config['SECRET_KEY'] = ''
        CORS(app, expose_headers=["Access-Token", "Uid", "Content-Disposition"])
        app.config['BUNDLE_ERRORS'] = True
        json_encoder = AlchemyEncoder
        app.json_encoder = json_encoder
        app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
        global api
        api = Api(app, catch_all_404s=True)

        # app.config['SECRET_KEY'] = config.secret_key
        init_api_resources(api)
        return app
    except Exception as e:
        print('Error')

app = create_app()

@app.teardown_appcontext
def shutdown_session(exception=None):
    print('Session was closed')
    session.remove()

# start application
if __name__ == '__main__':
    if (dev_mode == 'prod'):
        app.run(host='0.0.0.0')
    elif (dev_mode == 'dev'):
        app.run(debug=True, threaded=True)
    elif (dev_mode == 'win_dev'):
        app.run(debug=True, threaded=True)
