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

class TemplateAutoView(TemplateView):
    def get_template_names(self):
        return 'user/'+self.kwargs['template_name']+'.html'


urlpatterns = [
    url(r'^tp/(?P<template_name>\w+).html$', TemplateAutoView.as_view()),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^(index/|dashboard/)?$', DashboardView.as_view(),name='dashboard'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^passwd/$', PasswdView.as_view(), name='passwd'),
    url(r'^password/$', PasswordView.as_view(), name='password'),
    url(r'^nodes/$', NodeListView.as_view(), name='nodes')
]