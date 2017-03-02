#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: ‘wang_pc‘
@site: 
@software: PyCharm
@file: authentication.py
@time: 2017/3/1 21:19
'''
from user.models import User
from django.contrib.auth.backends import ModelBackend

class EmailUsernameAuthBackend(ModelBackend):

    def authenticate(self, user_auth_field, password, **kwargs):
        try:
            if '@' in user_auth_field:
                user = User.objects.get(email= user_auth_field)
            else:
                user = User.objects.get(username= user_auth_field)
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            pass
        else:
            if user.check_password(password):
                    return user




