#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: __init__.py.py 
@time: 2018/01/16 
"""
from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import errors, views
