#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: models.py 
@time: 2018/01/16 
"""


class User(object):
    id = None
    name = None
    password = None
    email = None
    role = None
    avatar = None
    last_login = None

    @property
    def is_authorization(self):
        return True

    @property
    def is_authenticated(self):
        return True
