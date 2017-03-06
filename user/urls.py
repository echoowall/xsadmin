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

app_name = 'user'

urlpatterns = [
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^(index/|dashboard/)?$', DashboardView.as_view(),name='dashboard'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^passwd/$', PasswdView.as_view(), name='passwd'),
    url(r'^password/$', PasswordView.as_view(), name='password'),
    url(r'^nodes/(?P<tag_slug>[\w-]+)?$', NodeListView.as_view(), name='nodes'),
    url(r'^node_qr_info/$', NodeQrInfoView.as_view(), name= 'node_qr_info'),
    url(r'^post_detail/(?P<pk>\d+)$', PostDetailView.as_view(), name= 'post_detail'),
    url(r'^posts/$', PostListView.as_view(), name='posts'),
]

menus = (
    {'title': '仪表盘', 'title_en': 'Dashboard', 'icon': 'dashboard', 'url_name': 'user:dashboard', 'children': ()},
    {'title': '用户中心', 'title_en': 'User Center','icon': 'user', 'url_name': '', 'children': (
        {'title': '我的信息', 'title_en': 'My Profile', 'icon': 'users', 'url_name': 'user:profile'},
        {'title': '安全设置', 'title_en': 'Safe Setting', 'icon': 'user-secret', 'url_name': 'user:password'},
        {'title': '连接设置', 'title_en': 'Connection Setting', 'icon': 'connectdevelop', 'url_name': 'user:passwd'},
    )},
    {'title': '节点中心', 'title_en': 'Node Center', 'icon': 'codepen', 'url_name': 'user:nodes', 'children': ()},
    {'title': '站内通告', 'title_en': 'Site Notice', 'icon': 'comment', 'url_name': 'user:posts', 'children': (
        {'title': '通告详情', 'title_en': 'Notice Detail', 'icon': 'comment', 'url_name': 'user:post_detail', 'no_reverse': True},
    )},
)