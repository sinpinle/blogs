#!/usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:yunzju 
@file: weibo.py 
@time: 2018/01/18 
"""
import requests


class APIError(Exception):
    def __init__(self, err='调用微博接口异常'):
        Exception.__init__(self, err)


class WBConfig(object):
    APP_KEY = '151163143'
    APP_SECRET = '87d620367740a17f9cd4b016a7e8d7ec'

    API_CALL_URL = 'https://api.weibo.com/oauth2'
    REDIRECT_URL = 'http://127.0.0.1:5000/admin/oauth'

    API_CALL_USER_URL = 'https://api.weibo.com/2/users/show.json'

    AUTHORIZE = '/authorize'
    ACCESS_TOKEN = '/access_token'
    GET_TOKEN_INFO = '/get_token_info'
    REVOKEOAUTH2 = '/revokeoauth2'

    @staticmethod
    def dict_param(data):
        url_params = '?'
        for key in data.keys():
            url_params += '%s=%s&' % (key, data[key])
        return url_params

    @staticmethod
    def call_api(method, params, call_type='', url=API_CALL_URL, is_redirect=False):
        base_url = url + call_type
        if method == 'get' or method == 'GET':
            url_params = WBConfig.dict_param(params)
            call_url = base_url + url_params
            if is_redirect:
                return call_url
            else:
                return requests.get(call_url)
        elif method == 'post' or method == 'POST':
            return requests.post(base_url, params)
        else:
            raise APIError()

    def authorize(self):
        params = {'client_id': self.APP_KEY, 'redirect_uri': self.REDIRECT_URL, 'response_type': 'code'}
        return WBConfig.call_api(call_type=self.AUTHORIZE, method='get', params=params, is_redirect=True)

    def access_token(self, code):
        params = {'client_id': self.APP_KEY, 'client_secret': self.APP_SECRET,
                  'grant_type': 'authorization_code', 'code': code,
                  'redirect_uri': self.REDIRECT_URL}
        result = WBConfig.call_api(call_type=self.ACCESS_TOKEN, method='post', params=params)
        return result

    def get_token_info(self, access_token):
        params = {'access_token': access_token}
        result = WBConfig.call_api(call_type=self.GET_TOKEN_INFO, method='post', params=params)
        return result

    def revoke_auth(self, access_token):
        params = {'access_token': access_token}
        result = WBConfig.call_api(call_type=self.REVOKEOAUTH2, method='post', params=params)
        return result

    def get_user_info(self, access_token, uid):
        url = self.API_CALL_USER_URL
        params = {'access_token': access_token, 'uid': uid}
        result = WBConfig.call_api(url=url, params=params, method='get')
        return result


if __name__ == '__main__':
    wb = WBConfig()
    wb.authorize()
