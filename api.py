from flask import Flask
from flask_restful import Resource, Api
from json_encoder import AlchemyEncoder
#init application
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
json_encoder = AlchemyEncoder
app.json_encoder =json_encoder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
api = Api(app)

#import resources
from res.user_roles_resources import *
from res.client_types_resources import *
from res.clients_resources import *
from res.users_resources import *
from res.user_logins_resources import *
from res.log_resources import *
from res.upload_resources import *
#add resources
#user roles
api.add_resource(UserRoleListResource, '/userRoles', endpoint='user-roles')
api.add_resource(UserRoleResource, '/userRole/<int:id>', endpoint='user-role')

#client types
api.add_resource(ClientTypeListResource, '/clientTypes', endpoint='client-types')
api.add_resource(ClientTypeResource, '/clientType/<int:id>', endpoint='client-type')

#clients
api.add_resource(ClientListResource, '/clients', endpoint='clients')
api.add_resource(ClientResource, '/client/<int:id>', endpoint='client')

#users
api.add_resource(UserListResource, '/users', endpoint='users')
api.add_resource(UserResource, '/user/<int:id>', endpoint='user')

#user logins
api.add_resource(UserLoginListResource, '/userLogins', endpoint='usersLogins')
api.add_resource(UserLoginResource, '/userLogin/<int:id>', endpoint='userLogin')
api.add_resource(UserAuthResource, '/login', endpoint='login')

#log
api.add_resource(LogListResource, '/log', endpoint='log')

#upload files
api.add_resource(UploadFile, '/upload', endpoint='upload')

#start application
if __name__ == '__main__':
    #u_s.get_user_roles()
    app.run(debug=True)