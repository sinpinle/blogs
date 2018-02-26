#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: errors.py 
@time: 2018/01/21 
"""
from flask import render_template
from app import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error={'title': 'Not Found', 'msg': 'Page Not Found ', 'detail': e}), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error={'title': 'Server Error', 'msg': 'Server Occur Error', 'detail': e}), 500
