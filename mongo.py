#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: mongo.py 
@time: 2018/01/20 
"""

import os
import urllib.parse
from pymongo import MongoClient


class MongodbConfig(object):
    MONGODB_USER = os.getenv('MONGO_USER', 'xxxx')
    MONGODB_PWD = os.getenv('MONGO_PWD', 'xxxxx')
    USERNAME = urllib.parse.quote_plus(MONGODB_USER)
    PASSWORD = urllib.parse.quote_plus(MONGODB_PWD)
    MONGODB_DEFAULT_URL = 'mongodb://%s:%s@127.0.0.1:27017/blog' % (USERNAME, PASSWORD)
    MONGODB_URL = os.getenv('MONGODB_URL', MONGODB_DEFAULT_URL)
    MONGODB_DB = 'blog'

    ENV_PRODUCT = {'M_URL': MONGODB_URL}
    ENV_TEST = {'M_URL': MONGODB_URL}

    def __init__(self, profile='default'):
        if profile == 'production' or profile == 'product':
            self.config = self.ENV_PRODUCT
        elif profile == 'test' or profile == 'default':
            self.config = self.ENV_TEST
        self._create_client()

    def _create_client(self):
        client = MongoClient(self.config.get('M_URL'), connect=False)
        m_db = client.get_database(name=self.MONGODB_DB)
        self.mdb = m_db


if __name__ == '__main__':
    mc = MongodbConfig('product')
    print(mc.config)
    mdb = mc.mdb
    blog = mdb.get_collection('blog')
