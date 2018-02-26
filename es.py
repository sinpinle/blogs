#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: es.py 
@time: 2018/02/11 
"""
from elasticsearch import Elasticsearch

# body = {'name': 'sinpinle', 'sex': 'male'}
body = {'content': 'this is a test of elasticsearch', 'date': '2018-02-11'}
es = Elasticsearch([''])

# es.index(index='test', doc_type='test', body=body)
# re = es.index(index='article', doc_type='test', body=body)
# print(re)

p = es.search(index='article', doc_type='test',
              body={'query': {'match': {'content': 'tes'}}, 'highlight': {'fields': {'date': {}}}})
print(p)
