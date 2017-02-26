#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/2/26 16:15
'''
from . import settings

#开发环境下的自定义设置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xsadmin',
        'USER':'root',
        'PASSWORD':'',
        'HOST':'127.0.0.1',
        'PORT':'3306'
    }
}