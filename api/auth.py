#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/3/8 0:08
'''
from rest_framework import authentication

class MyAPISignatureAuthentication(authentication.BaseAuthentication):


    def authenticate_header(self, request):

        pass


    def authenticate(self, request):
        pass
