#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/2/27 14:20
@desc: 工具类
'''
import uuid,hashlib,random

def md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()

def gen_passwd():
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',10))

def gen_val_code():
    return ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ',8))

def gen_api_key():
    return md5(uuid.uuid4().__str__())

def gen_api_secret():
    return md5(uuid.uuid4().__str__())

def gen_invite_code():
    return md5(uuid.uuid4().__str__())

if __name__ == '__main__':
    print ('md5',md5('123'))
    print('passwd',gen_passwd())
    print('val_code',gen_val_code())
    print('api_key',gen_api_key())
    print('api_secret',gen_api_secret())
    print('invite_code',gen_invite_code())