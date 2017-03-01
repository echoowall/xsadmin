#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: ‘wang_pc‘
@site: 
@software: PyCharm
@file: authentication.py
@time: 2017/3/1 21:19
'''
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class EmailUsernameAuthBackend(ModelBackend):

    def authenticate(self, user_auth_field=None, password=None, **kwargs):
        UserModel = get_user_model()
        if user_auth_field is not None and password is not None:
            user_set = UserModel._default_manager.filter(Q(username__exact=user_auth_field)|Q(email__exact=user_auth_field))
            if user_set.count() == 1:
                user = user_set[0]
                if user.check_password(password):
                    return user



