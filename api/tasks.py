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

from user.models import User, TrafficRecord
from django.db.models import When, Case, F, Value
from datetime import datetime
import logging

@periodic_task(name='重置所有用户已使用流量', run_every= crontab(hour=0, minute=0, day_of_month=1))
def reset_all_users_transfer():
    User.objects.update(u=0, d=0)

@shared_task(name='从节点API传来的流量数据更新到数据库')
def update_users_transfer(data_list, node):
    logging.info('准备更新流量啦：%s' % data_list)
    #批量插入
    traffic_list = list()
    case_u = list()
    case_d = list()
    ports = data_list.keys()
    for port in ports:
        trans = data_list[port]
        u = trans[0]
        d = trans[1]
        rate = node['node_rate']
        traffic_list.append(TrafficRecord(u=u, d=d, rate=rate,
                              node_id=node['node_id'], port=port))
        case_u.append(When(port=port, then=F('u')+u*rate/100))
        case_d.append(When(port=port, then=F('d')+d*rate/100))
    TrafficRecord.objects.bulk_create(traffic_list)
    #批量更新
    User.objects.filter(port__in=ports).update(u=Case(default=F('u'), *case_u),
                                               d=Case(default=F('d'), *case_d),
                                               t=datetime.now().timestamp())



@shared_task(name='打印日志')
def logging_info(arg):
    logging.info(arg)

'''
@periodic_task(name='打印日志任务', run_every= crontab(hour="*", minute="*", day_of_month="*"))
def logging_info_task():
    logging.info('我是打印日志任务')
'''


