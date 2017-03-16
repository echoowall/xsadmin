#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/3/10 14:24
'''
from django.db.models import Q,F
from user.models import User
from api.tasks import update_users_transfer
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger('xsadminloger')

def update_transfer_fetch_users(data, node):
    if data:  #如果没有传过来流量，我们不处理
        update_users_transfer.delay(data, node)
        #update_users_transfer(data, node)
    user_ports_data = cache.get('user_ports_data')
    if user_ports_data is None:
        user_ports_data = User.objects.filter(transfer_enable__gt=F('u') + F('d'), switch=True,
              is_active=True).extra(select={'password': 'passwd'}).values('port', 'password')
        user_ports_data = list(user_ports_data)
        cache.set('user_ports_data', user_ports_data, timeout=settings.USER_PORTS_CACHE_TIME)
        logger.info('set user_ports_data cache:%s'%user_ports_data)
    return user_ports_data