#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/3/7 21:32
'''

from user.models import *
from rest_framework import serializers

class UserPortSerializer(serializers.Serializer):
    port = serializers.IntegerField(read_only= True)
    passwd = serializers.CharField(read_only= True)
