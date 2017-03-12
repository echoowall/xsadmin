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
from django.db.models import When, Case, F, Sum, fields
from datetime import datetime, timedelta
from django.utils import timezone
import logging

@periodic_task(name='重置所有用户已使用流量', run_every= crontab(minute=0, hour=0, day_of_month=1))
def reset_all_users_transfer():
    User.objects.update(u=0, d=0)

@periodic_task(name='用户流量记录汇总', run_every= crontab(minute=30, hour=3))
def reset_all_users_transfer():
    # 1.每天凌晨汇总用户昨天使用的流量
    yesterday = timezone.now() - timedelta(days=1)
    traffic_list = TrafficRecord.objects.filter(create_date=yesterday).values('port', 'node_id')\
        .annotate(sum_u=Sum(F('u') * F('rate') / 100, output_field=fields.IntegerField()),
        sum_d=Sum(F('d') * F('rate') / 100, output_field=fields.IntegerField())).order_by()
    tr_list = list()
    for traf in traffic_list:
        #print(traf)
        tr = TrafficRecord(u=traf['sum_u'], d=traf['sum_d'], type=1, port=traf['port'],
                           summary_date=yesterday, node_id=traf['node_id'])
        tr_list.append(tr)
    TrafficRecord.objects.bulk_create(tr_list)
    # 2.删除7天前的流量记录，防止表数据过大
    TrafficRecord.objects.filter(summary_date__lte=timezone.now() - timedelta(days=7)).delete()

@shared_task(name='从节点API传来的流量数据更新到数据库')
def update_users_transfer(data_list, node):
    #logging.info('准备更新流量啦：%s' % data_list)
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


