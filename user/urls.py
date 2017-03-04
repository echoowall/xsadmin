#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/2/26 18:23
'''

from django.conf.urls import url
from .views import *
from django.views.generic import TemplateView
from django.urls import reverse_lazy

class TemplateAutoView(TemplateView):
    def get_template_names(self):
        return 'user/'+self.kwargs['template_name']+'.html'

app_name = 'user'

urlpatterns = [
    url(r'^tp/(?P<template_name>\w+).html$', TemplateAutoView.as_view()),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^(index/|dashboard/)?$', DashboardView.as_view(),name='dashboard'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^passwd/$', PasswdView.as_view(), name='passwd'),
    url(r'^password/$', PasswordView.as_view(), name='password'),
    url(r'^nodes/$', NodeListView.as_view(), name='nodes'),
    url(r'^node_qr_info/$', NodeQrInfoView.as_view(), name= 'node_qr_info')
]

menus = (
    {'title': '仪表盘', 'title_en': 'Dashboard', 'icon': 'dashboard', 'url': reverse_lazy('user:dashboard'), 'children': ()},
    {'title': '用户中心', 'title_en': 'User Center','icon': 'user', 'url': '', 'children': (
        {'title': '我的信息', 'title_en': 'My Profile', 'icon': 'users', 'url': reverse_lazy('user:profile')},
        {'title': '安全设置', 'title_en': 'Safe Setting', 'icon': 'user-secret', 'url': reverse_lazy('user:password')},
        {'title': '连接设置', 'title_en': 'Connection Setting', 'icon': 'connectdevelop', 'url': reverse_lazy('user:passwd')},
    )},
    {'title': '节点中心', 'title_en': 'Node Center', 'icon': 'codepen', 'url': reverse_lazy('user:nodes'), 'children': ()},
)