#!/usr/bin/python
#-*- coding:utf-8 -*-
# BY :   H .c
import json
import requests
import certifi
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from lyh_project.settings import API

# salt_api = 'https://192.168.1.8:8001/'
class SaltApi(object):
    def __init__(self,url ):
        self.api = API
        self.url = url
        self.username = 'saltapi'     # 用户名
        self.password = '123'   # 密码
        self.headers = {    # 请求的头部信息
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Content-type': 'application/json'  # 固定的写法，Agent的浏览器参数
        }
        self.params = {'client':'local', 'fun':'', 'tgt':''}   # 这是 salt-api 固定key值
        self.login_url = self.api + 'login'    # 拼接路径
        self.login_params = {
            'username': self.username,
            'password': self.password,
            'eauth': 'pam'
        } #  将登录的信息封装成一个字典
        self.token = self.get_data(self.login_url, self.login_params).get('token')   #这段用了get_datat 方法
        # print (self.token)
        self.headers['X-Auth-Token'] = self.token   # 写入  token 信息

    def get_data(self, url, params):
        send_data = json.dumps(params)   # 先转换成json
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        response = request.json()   # 将字符串的返回值转换成json格式  给 response
        result = dict(response)   #转成可用的字典
        return result['return'][0]

    def  salt_command(self,  method, tgt, arg=None):
        if arg :
            params = {'client':'local', 'fun':method, 'tgt':tgt, 'arg':arg}
        else:
            params = {'client':'local', 'fun':method, 'tgt':tgt}
        result = self.get_data(self.url, params)
        return result