#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: forms.py 
@time: 2018/01/16 
"""

from flask_wtf import FlaskForm as Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(), Length(6, 20)])
    password = StringField('password', validators=[DataRequired(), Length(6, 25)])
    remember_me = BooleanField('remember_me', default=False)
