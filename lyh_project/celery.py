#!/usr/bin/python
#-*- coding:utf8 -*-
#BY:  H.c
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lyh_project.settings')
app = Celery('lyh_project')    #这里的字符串要和 当前的目录名一致

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print ('Request:  {0!x}'.format(self.request))