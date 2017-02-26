#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/2/26 18:30
@described：用户站点自定义设置
'''

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '05bk@wyb%nm2-=59n08-mu@^t7+#%x$^kk8_%pm_wcnq6ga!2='

ALLOWED_HOSTS = []
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
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

SITE_CONFIG = {
    'SITE_NAME':'XS Admin',
    'SITE_DESC':'One powerful tool...',
}