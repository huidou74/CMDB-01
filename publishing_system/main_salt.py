#!/usr/bin/python
#-*- coding:utf-8 -*-
# BY :   H .c
import os,sys
import time
import json
import salt.client as sc
import salt.loader as salt_loader
import salt.config
import subprocess
import datetime
from celery.result import AsyncResult
from lyh_project.celery import app


class UtcTime(object):

    def __init__(self, after='',**kwargs):
        self.year = kwargs.get('year')
        self.month = kwargs.get('month')
        self.day = kwargs.get('day')
        self.hour = kwargs.get('hour')
        self.minute = kwargs.get('minute')
        self.after = after * 60
        self.date_time = datetime.datetime  # 作为内存地址来用的变量

    def ctime(self):     #  年月日时分秒
        ctime = self.date_time(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute).timestamp()
        return self.date_time.utcfromtimestamp(ctime)

    def after_time(self):   #  几分钟后
        utc = self.date_time.utcfromtimestamp(self.date_time.now().timestamp())
        return (utc + datetime.timedelta(seconds=self.after))



class MainSalt(object):  # salt 代码
    def __init__(self, tgt='*'):
        self.local = sc.LocalClient()
        self.tgt = tgt

    def get_cache_returns(self, func):
        while not self.local.get_cache_returns(func):
            time.sleep(1)
        return self.local.get_cache_returns(func)

    def cmd_run(self, run_func):
        if not isinstance(run_func, list):
            # 请求的数据类型错误
            raise TypeError(AttributeError)
        cmd_id = self.local.cmd_async(self.tgt, 'cmd.run', run_func)
        ret_cmd = self.get_cache_returns(cmd_id)
        return ret_cmd

    def state(self, salt_fun, tag=''):

        if tag:
            disk_id = self.local.cmd_async(self.tgt, 'state.sls', [salt_fun, tag])
            # 实际上 把信息塞入ZeroMq 返回一个ID
            # print (disk_id)
        else:
            disk_id = self.local.cmd_async(self.tgt, 'state.sls', [salt_fun, ])
        ret_disk_data = self.get_cache_returns(disk_id)
        return ret_disk_data

    def push_package(self, pillar_dic):
        tag = 'pillar={0}'.format(json.dumps(pillar_dic))  # 字典转JSON格式
        salt_fun = 'test'  # test.sls   就是状态管理里面的这个文件 加载
        return self.state(salt_fun, tag)



def sub_run(cmd):
    return  subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # 这个返回的对象，有两个方法。来判断是否正确执行 stdout和 stderr