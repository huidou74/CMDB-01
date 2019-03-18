#!/usr/bin/python
#-*- coding:utf8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from publishing_system.salt_run import run_salt_cmd,Salt_Run
@shared_task
def mian_salt(hosts_list):
    JG = Salt_Run(hosts_list)
    return JG.run_list()


@shared_task
def add(x, y):
    return x + y  # 定义自己的推送代码

@shared_task
def xsun(numbers):
    print(sum(numbers))
    return sum(numbers)