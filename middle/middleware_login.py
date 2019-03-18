#!/usr/bin/python
#-*- coding:utf8 -*-
#BY:  H.c
# Ctrl+B  跳转查看源代码
# from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import redirect, HttpResponse      #路由返回
from lyh_project.settings import white_list,AUTH_LIST   # 白名单列表的引入
import re

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class Middleware_login(MiddlewareMixin):
    def process_request(self, request):
        if not request.META.get('PATH_INFO') in white_list:
            if not request.session.get('login') :
                return redirect('/login/')


class Middleware_auth(MiddlewareMixin):
    def process_request(self, request):
        current_url = request.path_info
        # print ('当前的url  --->   ',current_url)   # 取 当前的访问的 url

        # 白名单设置    有BUG  还有填写表单，删除也的确定弹窗 要加载样式
        for i in AUTH_LIST:
            if re.match(i, current_url):    # 匹配白名单，匹配不到 就返回 空，不走if里面的内容
                return None    #  匹配 中了 就往 视图 走

        # 取session信息 并判断
        auth_dict = request.session.get('auth_dict')  # 取 当前请求的 session 信息
        # print('session 信息 ---> ',auth_dict)
        if not auth_dict:    # Not + (取不到值就为空，取到了就是true)  # 负负得正走if 的内容，负正跳过当前if 判断
            return redirect('/authority/demo/')    # 跳去权限登录页面

        flag = False   # 打标记开关

        for group_name, auth_url in auth_dict.items():   # 取到的是个字典，用for循环可以吧items的key和values拿出来用
            for url in auth_url.get('url'):    # 因为一个K和V的字典，所用直接get values 才能 来循环里面的url
                # print ('--------- url的拼接 ----------')
                # print(url) # url
                regax = "^{0}$".format(url)    # 将它拼接
                # print (regax) # 拼接的结果
                if re.match(regax, current_url): # 循环判断数据库里的url。  再用re 模块来判断它是否匹配该当前的url
                    request.permission_code_list = auth_url['url']  #往request里面增加数据,增加的数据是匹配的数据
                    # print (request.permission_code_list)
                    flag = True  # 打开标志，停止当前循环
                    break
            if flag:   # 标志位为 True 联动开关，停止循环
                break
        # print(request.permission_code_list)
        # print(request.path_info)   当前访问的 url
        # print(request.session['login'])  # 用户 session
        # print(request.session['auto_user']) # 权限用户 session
        if request.session.get('auto_user'):
            flag = True    # 判断用户的权限 session  有则 强制吧标志位转换， 让请求走到路由

        if not flag:  # 如果上面的匹配没通过，则 标志位不变，即为 无权限用户，跳转至提示页面
            return HttpResponse('该用户无权访问')
            















