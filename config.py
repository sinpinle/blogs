#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: config.py 
@time: 2018/01/16 
"""
import os
from mongo import MongodbConfig


class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

    _SYS_PROFILE = os.getenv('active.profile', 'production')  # 判断测试或者生产环境
    _MONGODB_CFG = MongodbConfig(_SYS_PROFILE)

    mongodb = _MONGODB_CFG.mdb
