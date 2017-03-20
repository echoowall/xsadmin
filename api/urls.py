#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/3/7 21:37
'''

from .views import *
from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'user_port': reverse('api:user_port', request=request, format=format),
    })

urlpatterns = [
    url(r'^$', api_root),
    url(r'^user_port/$', UserPortView.as_view(), name='user_port'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^wechat/$', WeChatView.as_view(), name='wechat'),
]
