#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/3/10 12:16
'''

from django.db.models import signals
from django.dispatch import receiver
from .models import *
import logging
from .utils import refush_node_app_keyset

'''
@receiver(signals.post_save, sender=Node)
def welcome_student(instance, **kwargs):
    instance.__original_name = instance.name

@receiver(signals.post_save, sender=Student)
def welcome_student(instance, created, **kwargs):
    if not created and instance.__original_name != instance.name:
        Announcement.objects.create(content=
            'Student %s has renamed to %s' % (instance.__original_name, instance.name))
'''

logger = logging.getLogger('xsadminloger')

@receiver(signals.post_save, sender=Node)
def on_node_save(instance, created, **kwargs):
    #logger.info('on_node_save:node changed!')
    refush_node_app_keyset()
