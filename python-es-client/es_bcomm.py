# coding=utf-8

"""
@author: 尹学峰
@license: (C) Copyright 2019-2029, Rancher Labs.
@contact: 
@software: pycharm
@file: es_bcomm.py
@time: 2019/10/13 10:38
@desc:
"""

import os
import time
from os import walk
import csv
import json
from datetime import datetime
from elasticsearch6 import Elasticsearch
from elasticsearch6.helpers import bulk


class ElasticBcomm:

    def __init__(self, index_name, index_type, ip="127.0.0.1",port='9200'):
        '''

        :param index_name: 索引名称
        :param index_type: 索引类型
        '''
        self.index_name = index_name
        self.index_type = index_type
        self.es = Elasticsearch([ip], port=port)

    def create_index(self):
        '''
        创建索引,创建索引名称为app_es_201909，类型为user_info的索引
        :param ex: Elasticsearch对象
        :return:
        '''
        #创建映射
        _index_mappings = {
            "mappings": {
                self.index_type: {
                    "properties": {
                        "appl_date": {
                            "type": "text",
                            "index": True
                        },
                        "card_apply_no": {
                            "type": "text"
                        },
                        "comp_addr": {
                            "type": "text"
                        },
                    }
                }

            }
        }
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=_index_mappings)
            print(res)


    def Index_Data(self, data_list):
        '''
        数据存储到es
        :return:
        '''
        for item in data_list:
            res = self.es.index(index=self.index_name, doc_type=self.index_type, body=item)
            # print(res['created'])
            print(res)

    def Delete_Index_Data_By_Id(self,id):
        '''
        删除索引中的一条
        :param id:
        :return:
        '''
        res = self.es.delete(index=self.index_name, doc_type=self.index_type, id=id)
        print (res)

    def Delete_Index(self):
        '''
        删除index
        '''
        res = self.es.indices.delete(index=self.index_name, ignore=[400, 404])
        print (json.dumps(res, indent=2))

    def Get_Data_By_Id(self,id):

        res = self.es.get(index=self.index_name, doc_type=self.index_type,id=id)
        print(res['_source'])

        print ('------------------------------------------------------------------')

    def Get_Data_By_Body(self):
        # doc = {'query': {'match_all': {}}}
        doc = {"query": {"bool": {"must": [{"match_all": {}}], "must_not": [], "should": []}}, "from": 0, "size": 10,
                "sort": [], "aggs": {}}
        _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=doc)
        for hit in _searched['hits']['hits']:
            print(hit)


obj = ElasticBcomm("app_es_201909","user_info",ip ="47.75.181.169",port='32454')
#删除索引
# obj.Delete_Index()

#按查询参数查询
# obj.Get_Data_By_Body()

#按id查询
# obj.Get_Data_By_Id("yG3cym0BO6_4vkZPfzl_")

#创建索引
# obj.create_index()
# list = [
#     {
#         "appl_date": "2019-09-11",
#         "card_apply_no": "20190801555665196710070003",
#         "comp_addr": "深圳"
#     }
# ]
# obj.Index_Data(list)

obj.Get_Data_By_Body()
# obj.GetData(es)
