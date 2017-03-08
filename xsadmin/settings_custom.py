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
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_TRANSPORT = 'redis'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

STATIC_ROOT = "/var/www/example.com/static/"

SITE_CONFIG = {
    'SITE_NAME':'XS Admin',
    'SITE_DESC':'One powerful tool...',
}

#极验证
GEE_CAPTCHA_ID = 'b46d1900d0a894591916ea94ea91bd2c'
GEE_PRIVATE_KEY = '36fc3fe98530eea08dfc6ce76e3d24c4'

# import django
# django.setup()
#import djcelery
#djcelery.setup_loader()

