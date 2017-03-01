#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: ‘wang_pc‘
@site: 
@software: PyCharm
@file: forms.py
@time: 2017/3/1 16:21
'''
from django import forms
from django.forms import fields
from django.forms import widgets
from django.urls import resolvers
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    userfield = fields.CharField(required=True,max_length=64,
        widget= widgets.TextInput(attrs={'class': 'form-control','placeholder': '用户名/邮箱'}))
    password = fields.CharField(required=True,max_length=64,min_length=8,
        widget= widgets.PasswordInput(attrs={'class': 'form-control','placeholder': '登录密码'}))
    remember = fields.BooleanField(required=False)

    error_messages = {
        'invalid_login': '用户 %(username)s 不存在或密码错误',
        'inactive':'用户 %(username)s 未激活',
        'invalid_field':'请输入登陆账号和密码',
    }


    def __init__(self, *args, **kwargs):
        super(LoginForm,self).__init__(*args, **kwargs)

    def clean(self):
        userfield = self.cleaned_data.get('userfield')
        password = self.cleaned_data.get('password')

        if userfield and password:
            self.user_cache = authenticate(user_auth_field=userfield, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': userfield},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                    params={'username': userfield},
                )
        else:
           raise forms.ValidationError(
                    self.error_messages['invalid_field'],
                    code='invalid_field',
                )
        return self.cleaned_data



