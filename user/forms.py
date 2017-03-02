#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/3/2 20:23
'''
from django.forms import Form,ModelForm,fields,widgets,ValidationError
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from django.contrib.auth import update_session_auth_hash


class ProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit','确定修改'))

    class Meta:
        model = User
        fields = ('first_name','last_name','avatar')

class PasswdForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit','确定修改'))

    class Meta:
        model = User
        fields = ('passwd',)
        help_texts = {'passwd': '连接密码，修改后，可能需要稍等几分钟才能生效'}

class PasswordForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit','确定修改'))

    old_password = fields.CharField(required=True, max_length=128, min_length=8,label='旧密码',
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '旧密码'}))
    password = fields.CharField(required=True, max_length=128, min_length=8,label='新登录密码',
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '新登录密码'}))
    password2 = fields.CharField(required=True, max_length=128, min_length=8,label='确认新登录密码',
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '确认新登录密码'}))
    field_order = ('old_password', 'password', 'password2')

    class Meta:
        model = User
        fields = ('password',)

    def clean_old_password(self):
        user = self.instance
        old_pwd = self.cleaned_data['old_password']
        if user.check_password(old_pwd):
            return old_pwd
        else:
            raise ValidationError(message='旧密码不正确')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password == password2:
            return password2
        else:
            raise ValidationError(message='两次输入的密码不一致')

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user