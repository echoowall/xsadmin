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
from django.core.validators import EmailValidator,RegexValidator,ValidationError
from user.models import User,InviteCode
import datetime

username_regex = r'^\w+$'

class LoginForm(forms.Form):
    password = fields.CharField(required=True,max_length=64,min_length=8,
        widget= widgets.PasswordInput(attrs={'class': 'form-control','placeholder': '登录密码'}))
    userfield = fields.CharField(required=True,max_length=64,
        widget= widgets.TextInput(attrs={'class': 'form-control','placeholder': '用户名/邮箱'}))
    remember = fields.BooleanField(required=False, initial= {'default': True })

    def clean_userfield(self):
        userfield = self.cleaned_data.get('userfield')
        if '@' in userfield:
            EmailValidator()(userfield)
        else:
            RegexValidator(regex= username_regex, message='用户名不合法')(userfield)
        return userfield

    error_messages = {
        'invalid_login': '用户 %(username)s 不存在或密码错误',
        'inactive':'用户 %(username)s 未激活',
    }

    def clean(self):
        userfield = self.cleaned_data.get('userfield')
        password = self.cleaned_data.get('password')
        if userfield is not None and password is not None:
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
        return self.cleaned_data

class RegisterForm(forms.Form):
    username = fields.CharField(required=True, max_length=64, min_length=4,
            widget= widgets.TextInput(attrs={'class': 'form-control','placeholder': '用户名'}))
    email = fields.EmailField(required=True, max_length=128, min_length= 6,
            widget= widgets.EmailInput(attrs={'class': 'form-control','placeholder': '邮箱'}))
    password = fields.CharField(required=True, max_length= 128, min_length= 8,
        widget= widgets.PasswordInput(attrs={'class': 'form-control','placeholder': '登录密码'}))
    password2 = fields.CharField(required=True, max_length= 128, min_length= 8,
        widget= widgets.PasswordInput(attrs={'class': 'form-control','placeholder': '确认密码'}))
    invite_code = fields.CharField(required=True,max_length=64,min_length=8,
        widget= widgets.TextInput(attrs={'class': 'form-control','placeholder': '邀请码'}))

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password == password2:
            return password2
        else:
            raise forms.ValidationError(message='确认密码不正确')

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        try:
            code = InviteCode.objects.get(code__exact=invite_code)
            if code.enable:
                return invite_code
            else:
                raise forms.ValidationError(message='邀请码已被使用')
        except InviteCode.DoesNotExist or InviteCode.MultipleObjectsReturned:
            raise forms.ValidationError(message='邀请码不存在')




