import os
import inspect
from flask_restful import Resource
import modules.request_initializer as rq_init
# import resv2.user_roles_resources as user_roles

import importlib

tree = os.listdir('resv2')
module_names = [f.rsplit('.py')[0] for f in tree if f.rfind(".py") != -1]

# [resource_class]
api_resources_crud = []

for module_name in module_names:
    module = importlib.import_module('resv2.{}'.format(module_name))
    post_data_converter = getattr(module, 'post_data_converter', None)
    put_data_converter = getattr(module, 'put_data_converter', None)

    if hasattr(module, 'input_data_converter'):
        post_data_converter = module.input_data_converter
        put_data_converter = module.input_data_converter

    after_post_action = getattr(module, 'after_post_action', None)
    after_put_action = getattr(module, 'after_put_action', None)

    output_fields_dict = getattr(module, 'OUTPUT_FIELDS_DICT', {})

    api_resources_crud.append(
        type(module.NAME, (Resource,),
             {'__init__': rq_init.create_init(module.ROUTE + '/<int:id>', module.END_POINT),
              'get': rq_init.create_get(module.ENTITY_NAME, module.MODEL,
                                        output_fields_dict.get('get', module.OUTPUT_FIELDS)),
              'delete': rq_init.create_delete(module.ENTITY_NAME, module.MODEL),
              'put': rq_init.create_put(module.ENTITY_NAME, module.MODEL,
                                        output_fields_dict.get('put', module.OUTPUT_FIELDS),
                                        put_data_converter, after_put_action)}),
    )
    api_resources_crud.append(
        type(module.NAME_LIST, (Resource,),
             {'__init__': rq_init.create_init(module.ROUTE_LIST, module.END_POINT_LIST),
              'get': rq_init.create_get_list(module.ENTITY_NAME, module.MODEL,
                                             output_fields_dict.get('get-list', module.OUTPUT_FIELDS)),
              'post': rq_init.create_post(module.ENTITY_NAME, module.MODEL,
                                          output_fields_dict.get('post', module.OUTPUT_FIELDS),
                                          post_data_converter, after_post_action)})
    )

# [resource_class]
api_resources_cross = []

tree = os.listdir('cross_res')
module_names = [f.rsplit('.py')[0] for f in tree if f.rfind(".py") != -1]

for module_name in module_names:
    module = importlib.import_module('cross_res.{}'.format(module_name))
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, Resource) and obj.__name__ != 'Resource':
            api_resources_cross.append(obj)


def init_single_resource(api, resource, route, endpoint):
    api.add_resource(resource, route, endpoint=endpoint)
    pass


def init_api_resources(api):
    for crud_resource in api_resources_crud:
        ex = crud_resource()
        init_single_resource(api, crud_resource, ex.route, ex.end_point)
        pass

    for cross_resource in api_resources_cross:
        ex = cross_resource()
        init_single_resource(api, cross_resource, ex.route, ex.end_point)
        pass
