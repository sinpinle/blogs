#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: errors.py
@time: 2018/01/16 
"""

import json

from flask import abort
from flask import render_template
from flask import request

from app import dbutils
from . import main


@main.route('/gongyi')
def gong_yi():
    return render_template('gongyi.html')


@main.route('/')
@main.route('/index')
def index():
    posts = dbutils.get_normal_posts()
    total = len(posts)
    tags = dbutils.get_tags()
    return render_template('index.html', title='Home', posts=posts, tags=tags, total=total)


@main.route('/suggest')
def blog_suggestion():
    posts = dbutils.get_posts_condition_normal(query={'top': 1})
    total = len(posts)
    tags = dbutils.get_tags()
    return render_template('index.html', title='Home', posts=posts, tags=tags, total=total)


@main.route('/about')
@main.route('/resume')
def author_resume():
    post = dbutils.get_post('5a6f16fc9d689d29a8d3b35f')
    if post is None:
        abort(404)
    posts = dbutils.get_normal_posts()
    tags = dbutils.get_tags()
    return render_template('blog.html', title=post['title'], post=post, posts=posts, tags=tags)
    return render_template('')


@main.route('/blog/<blog_id>')
def browser_blog(blog_id):
    post = dbutils.get_one_post_normal(query={'_id': blog_id})
    if post is None:
        abort(404)
    posts = dbutils.get_normal_posts()
    tags = dbutils.get_tags()
    return render_template('blog.html', title=post['title'], post=post, posts=posts, tags=tags)


@main.route('/feed')
def get_feed():
    """fee rss"""
    rss = '''<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
        <channel>
            <title>sinpinle博客</title>
            <link>http://www.sinpinle.tk</link>
            <description>sinpinle's blog</description>
            <item>
                <title>推荐</title>
                <link>http://www.sinpinle.tk/suggest</link>
                <description>推荐文章</description>
            </item>
        </channel>
    </rss>
    '''
    return rss, 200, {'Content-Type': 'application/rss+xml'}


@main.route('/tag/<tag_id>')
def browser_tag(tag_id):
    tag = dbutils.get_one_tag(tag_id)
    if tag is None:
        abort(404)
    posts = dbutils.get_posts_condition_normal(query={'tag': tag['name']})
    tags = dbutils.get_tags()
    return render_template('index.html', title=tag['name'], posts=posts, tags=tags)


@main.route('/list')
def get_normal_posts():
    """页面展示"""
    posts = dbutils.get_normal_posts()
    return json.dumps(posts)


@main.route('/admin/list')
@dbutils.need_permission
def get_all_posts():
    """管理员编辑列表"""
    posts = dbutils.get_all_posts()
    return json.dumps(posts)


@main.route('/admin/create')
@dbutils.need_permission
def create_page():
    """新增页面"""
    tags = dbutils.get_tags()
    return render_template('edit.html', title='新建', edit=False, tags=tags)


@main.route('/admin/add', methods=['POST'])
@dbutils.need_permission
def add_blog():
    """新增一个博文"""
    post = request.get_data()
    blog = json.loads(post.decode(encoding="utf-8"))
    result = dbutils.create_post(post=blog)
    if result is not None and str('_id') is not None:
        dbutils.update_tag_count()  # 更新统计数据
        return json.dumps({'result': 'ok'})
    else:
        return json.dumps({'result': 'fail'})


@main.route('/admin/edit/<blog_id>')
@dbutils.need_permission
def edit_page(blog_id):
    """管理员编辑"""
    blog = dbutils.get_post(blog_id)
    tags = dbutils.get_tags()
    return render_template('edit.html', title='编辑', blog=blog, edit=True, tags=tags)


@main.route('/admin/top/<blog_id>')
@dbutils.need_permission
def set_top(blog_id):
    """置顶"""
    post = dict()
    post['top'] = 1
    dbutils.update_post(blog_id=blog_id, post=post)
    return json.dumps({'result': 'ok'})


@main.route('/admin/update/<blog_id>', methods=['POST'])
@dbutils.need_permission
def save_edit(blog_id):
    """提交修改"""
    post = request.get_data()
    blog = json.loads(post.decode(encoding="utf-8"))
    result = dbutils.update_post(blog_id=blog_id, post=blog)
    if result is not None and result['_id'] == blog_id:
        dbutils.update_tag_count()  # 更新统计数据
        return json.dumps({'result': 'ok'})
    else:
        return json.dumps({'result': 'fail'})
