import json

import pandas as pd

import datetime
from pandas.io.json import json_normalize
import modules.json_serializator as j_ser


# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper
def convert_to_short_data(data):
    try:
        n_items = []
        pop_array = [
            'day',
            'documentId',
            'included_in_description',
            'month',
            'processed',
            'typeId',
            'uid',
            'valueCreditMinusDebet',
            'valueDebetMinusCredit',
            'year',
            'typeName'
        ]
        header = data['rows'][0]['cells'][0]['tableData']['items'][0]
        locked_indexes = []

        index =0
        for header_item in header:
            for pop_element in pop_array:
                if (pop_element == header_item):
                    locked_indexes.append(index)
                    index+=1
                    break
            index+=1
        i = 0
        for item in data['rows'][0]['cells'][0]['tableData']['items']:

            if (i == 0):
                i += 1
                continue
            n_item = {}
            index = 0
            element_index = 0
            for element in item:
                t = index in locked_indexes
                if (t == True):
                    index += 1
                    continue
                key = header[index]
                n_item[key] = element
                # setattr(n_item,header[index],element)
                index += 1

            n_items.append(n_item)
            i += 1
            if (i % 1000):
                print(str(i) + '/' + str(len(data['rows'][0]['cells'][0]['tableData']['items'])))
        data['rows'][0]['cells'][0]['tableData']['items'] = n_items
        pass
    except Exception as e:
        pass


# optimeze document content
def optimize_document_content(content):
    try:
        original_length = len(content)
        data = json.loads(content)
        t = 'use_short_data' in data['rows'][0]['cells'][0]['tableData']
        if (t == True):
            if (data['rows'][0]['cells'][0]['tableData']['use_short_data'] == True):
                convert_to_short_data(data)
            else:
                return content
        else:
            return content
        # # t = json_normalize(data['rows'][0]['cells'][0]['tableData']['items'])
        # pop_array = [
        #     'document',
        #     'day',
        #     'documentId',
        #     'included_in_description',
        #     'month',
        #     'processed',
        #     'typeId',
        #     'uid',
        #     'valueCreditMinusDebet',
        #     'valueDebetMinusCredit',
        #     'year',
        #     'typeName'
        # ]
        #
        #
        # i = 0
        # items = []
        # for item in data['rows'][0]['cells'][0]['tableData']['items']:
        #     percent = round(100 * (i / len(data['rows'][0]['cells'][0]['tableData']['items'])), 2)
        #     print(str(percent) + '%')
        #     i += 1
        #     for pop_element in pop_array:
        #         del item[pop_element]
        #
        #
        #     el_array = ['analyticsCredit', 'analyticsDebet']
        #     for el in el_array:
        #         max_length = 10
        #         lst = str(item[el]).split('\n')
        #         if (len(lst) > 0):
        #             item[el] = lst[0]
        #
        #         # if (len(str(item[el]))>max_length):
        #         #
        #         #     item[el] =str(item[el][0:max_length])
        #         #     t=0
        #
        #
        #
        #     items.append(item)
        # data['rows'][0]['cells'][0]['tableData']['items'] = items
        optimized_content = json.dumps(data, ensure_ascii=False)
        print('opt done')
        optimized_content_length = len(optimized_content)
        #
        zip_k = 100 * (1 - round(optimized_content_length / original_length, 2))
        print('zipped K = ' + str(zip_k))
        return optimized_content

    except Exception as e:
        print('FUCK' + e)
        return content
