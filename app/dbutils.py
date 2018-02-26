#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: dbutils.py 
@time: 2018/01/21 
"""
import functools
import json
import pymongo
from datetime import datetime
from bson import ObjectId
from flask import session
from pymongo.results import UpdateResult
from pymongo.results import DeleteResult
from pymongo.results import InsertOneResult
from app import mdb

MDB_USER = 'user'
MDB_BLOG = 'blog'
MDB_COMMENT = 'comment'
MDB_TAG = 'tag'
MDB_TEST = 'test'


class JSONOutputError(Exception):
    """json输出装饰器"""

    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


def _process_object_id(list_):
    for p in list_:
        tmp = p['_id']
        if type(tmp) is ObjectId:
            p['_id'] = str(tmp)


def list_to_dict(list_):
    _process_object_id(list_)
    return json.dumps(list_)


def process_object_id(func):
    @functools.wraps(func)
    def process(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if type(result) == dict and '_id' in result.keys():
                result['_id'] = str(result.get('_id'))
                return result
            elif type(result) == UpdateResult:
                return result.raw_result
            elif type(result) == DeleteResult:
                return result.raw_result
            elif type(result) == InsertOneResult:
                return result.inserted_id
            elif type(result) == str:
                return result
            else:
                _li = [j for j in result]
                _process_object_id(_li)
                return _li
        except JSONOutputError as ex:
            raise ex

    return process


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_collection(coll):
    return mdb.get_collection(coll)


def set_default_value(blog):
    keys = blog.keys()
    if 'author' not in keys:
        blog['author'] = 'sinpinle'
    if 'status' not in keys:
        blog['status'] = 1
    if 'top' not in keys:
        blog['top'] = 0
    if 'post_date' not in keys:
        blog['post_date'] = get_current_time()


@process_object_id
def create_post(post):
    set_default_value(post)
    blog = get_collection(MDB_BLOG)
    return blog.insert_one(post)


@process_object_id
def update_post(blog_id, post):
    blog = get_collection(MDB_BLOG)
    post['status'] = 1
    post['modify_date'] = get_current_time()
    obj_id = ObjectId(blog_id)
    return blog.find_one_and_update(filter={'_id': obj_id}, update={'$set': post})


@process_object_id
def get_post(blog_id):
    blog = get_collection(MDB_BLOG)
    obj_id = ObjectId(blog_id)
    return blog.find_one({'_id': obj_id})


@process_object_id
def delete_post(blog_id):
    blog = get_collection(MDB_BLOG)
    obj_id = ObjectId(blog_id)
    modify_date = get_current_time()
    return blog.find_one_and_update(filter={'_id': obj_id}, update={'$set': {'modify_date': modify_date, 'status': -1}})


@process_object_id
def real_delete(blog_id):
    blog = get_collection(MDB_BLOG)
    obj_id = ObjectId(blog_id)
    return blog.delete_one(filter={'_id': obj_id})


@process_object_id
def get_one_post_normal(query=None):
    blog = get_collection(MDB_BLOG)
    if query is None:
        query = dict()
    if '_id' in query.keys():
        query['_id'] = ObjectId(query['_id'])
    query['status'] = 1  # 状态为正常的blog
    return blog.find_one(filter=query)


@process_object_id
def get_normal_posts():
    blog = get_collection(MDB_BLOG)
    query = dict()
    query['status'] = 1  # 状态为正常的blog
    all_blog = blog.find(query).sort('post_date', pymongo.DESCENDING)
    return all_blog


def update_tag_count():
    blog = get_collection(MDB_BLOG)
    search = blog.aggregate([{'$group': {'_id': '$tag', 'num_tutorial': {'$sum': 1}}}])
    result = [s for s in search]
    if result is not None:
        tag = get_collection(MDB_TAG)
        for b in result:
            tag.update_one({'name': b['_id']}, {'$set': {'count': b['num_tutorial']}})


@process_object_id
def get_posts_condition_normal(query=None):
    blog = get_collection(MDB_BLOG)
    if query is None:
        query = dict()
    query['status'] = 1  # 状态为正常的blog
    return blog.find(query)


@process_object_id
def get_all_posts():
    blog = get_collection(MDB_BLOG)
    all_blog = blog.find()
    return all_blog


@process_object_id
def get_tags():
    tag = get_collection(MDB_TAG)
    all_tag = tag.find()
    return all_tag


@process_object_id
def get_one_tag(_id):
    tag = get_collection(MDB_TAG)
    a_tag = tag.find_one({'_id': ObjectId(_id)})
    return a_tag


@process_object_id
def create_new_user(name, email, password="default", role='admin', avatar='default'):
    user = dict()
    user['name'] = name
    user['password'] = password
    user['email'] = email
    user['role'] = role
    user['avatar'] = avatar
    user['last_login'] = get_current_time()
    user_collection = get_collection(MDB_USER)
    return user_collection.insert_one(user)


@process_object_id
def get_user(name):
    user = get_collection(MDB_USER)
    return user.find_one(filter={'name': name})


@process_object_id
def update_user(user):
    uc = get_collection(MDB_USER)
    name = user['name']
    if name is None:
        raise Exception('用户名为空')
    user['last_login'] = get_current_time()
    ur = uc.find_one(filter={'name': name})
    if ur is not None:
        return uc.update_one(filter={'name': name}, update={'$set': user})
    else:
        return uc.insert_one(document=user)


def check_name_and_pwd(name, pwd):
    if name == '' or pwd == '':
        return False
    user = get_collection(MDB_USER)
    ur = user.find_one(filter={'name': name, 'password': pwd})
    return ur is not None


def get_role(name):
    ur = get_user(name)
    if ur is None:
        return None
    return ur.get('role')


def need_permission(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        name = session.get('current_user', None)
        if name is None:
            raise PermissionError('没有权限进行该操作')
        role = get_role(name)
        if role is not None and role == 'admin':
            return func(*args, **kwargs)
        else:
            raise PermissionError('没有权限进行该操作')

    return inner


if __name__ == '__main__':
    rt = get_normal_posts()
    print(type(rt))
    print(rt)
    for x in rt:
        print(x['tag'])
