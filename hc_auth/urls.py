#!/usr/bin/python
#-*- coding:utf8 -*-
#BY:  H.c
from django.conf.urls import url, include
from django.contrib import admin
from hc_auth import views

urlpatterns = [
    url(r'demo/$', views.auth_demo),
    url(r'index/', views.index),
    url(r'user_info/',views.user_info,name='user_info')
   
    ]