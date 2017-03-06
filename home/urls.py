#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/2/26 16:57
'''
from django.conf.urls import url
from .views import *

app_name = 'home'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(),name='login'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^get_gee_captcha/$', GeeCaptchaView.as_view(), name='get_gee_captcha'),
    url(r'^code\.html$', InviteCodeView.as_view(), name='invite_code'),
    url(r'^(?P<slug>[\w-]+)\.html$', PostPageView.as_view(), name= 'post_page'),
    url(r'^(index/)?$', PostPageView.as_view(), name='index'),
]
