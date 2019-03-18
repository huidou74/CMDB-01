#!/usr/bin/python
#-*- coding:utf8 -*-
#BY:  H.c

from django.conf.urls import url
from django.contrib import admin
from publishing_system import views

urlpatterns = [
    url(r'right_away/', views.publish),
    url(r'timing/', views.celery_status),  # 必须要写的路由
]
