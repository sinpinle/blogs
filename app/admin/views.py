#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: errors.py
@time: 2018/01/16 
"""
import json
from flask import render_template, redirect, url_for, request, session
from app import dbutils
from weibo import WBConfig
from . import admin
from .forms import LoginForm
from .models import User


@admin.route('/')
@admin.route('/index')
def index():
    name = session.get('current_user', None)
    if name is None:
        return redirect(url_for('admin.login'))
    user = User()
    user.name = name
    posts = dbutils.get_all_posts()
    total = len(posts)
    tags = dbutils.get_tags()
    return render_template('admin.html', title='Home', user=user, posts=posts, tags=tags, total=total)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    name = session.get('current_user', None)
    if name is not None:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_username = form.username.data
            pwd = form.password.data
            success = dbutils.check_name_and_pwd(current_username, pwd)
            if success:
                session['current_user'] = current_username
                dbutils.update_user({'name': current_username})
                return redirect(url_for('admin.index'))
            else:
                return render_template('login.html', title='Sign In', form=form)
    else:
        return render_template('login.html', title='Sign In', form=form)


@admin.route('/oauth', methods=['GET', 'POST'])
def login_oauth():
    code = request.args.get('code')
    wb = WBConfig()
    if code is not None:
        rt = wb.access_token(code=code)  # get user info from the third web
        if rt is not None and rt.status_code == 200:
            str_at = rt.text
            dict_at = json.loads(str_at)
            uid = dict_at['uid']
            atk = dict_at['access_token']
            session['access_token'] = atk
            user_info = wb.get_user_info(uid=uid, access_token=atk)
            if user_info is not None and user_info.status_code == 200:
                str_u = user_info.text
                dict_user = json.loads(str_u)
                name = dict_user['name']
                avatar = dict_user['profile_image_url']
                user = dict()
                user['name'] = name
                user['email'] = 'sinpinle@163.com'
                user['avatar'] = avatar
                session['current_user'] = name
                if name == 'sinpinle':
                    dbutils.update_user(user)
                    return redirect(url_for('admin.index'))
                else:
                    return redirect(url_for('admin.login'))
            else:
                return redirect(url_for('admin.login'))
        else:
            return redirect(url_for('admin.login'))
    return redirect(wb.authorize(), code=302)


@admin.route('/logout')
def logout():
    name = session.get('current_user', None)
    access_token = session.get('access_token', None)
    if name is not None:
        session.clear()
        if access_token is not None:
            wb = WBConfig()
            wb.revoke_auth(access_token)
        return redirect(url_for('admin.login'))
    else:
        raise PermissionError('非法操作')
