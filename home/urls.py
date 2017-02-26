#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/2/26 16:57
'''
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^(index/)?$', IndexView.as_view(),name='index'),
    url(r'^download/$', DownloadView.as_view(),name='download'),
    url(r'^about/$', AboutView.as_view(),name='about'),
]
