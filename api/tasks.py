#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory
@file: tasks.py
@time: 2017/3/8 20:31
@description: 
'''
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab

from user.models import User
import logging

@periodic_task(name='重置所有用户已使用流量', run_every= crontab(hour=0, minute=0, day_of_month=1))
def reset_all_users_transfer():
    User.objects.update(u=0, d=0)

@shared_task(name='从节点API传来的流量数据更新到数据库')
def update_users_transfer(list):
    logging.info('准备更新流量啦：%s' % list)
    for port,trans in list.items():
        try:
            user = User.objects.get(port=int(port))
            user.u += trans[0]
            user.d += trans[1]
            user.save()
        except (User.DoesNotExist,User.MultipleObjectsReturned):
            pass



