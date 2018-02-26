#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: __init__.py.py 
@time: 2018/01/16 
"""

from flask import Flask
from config import Config

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
# db = SQLAlchemy(app)
mdb = Config.mongodb

from .admin import admin as admin_blueprint
from .main import main as main_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')
