#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/3/8 0:08
'''
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
import re, hashlib
from datetime import datetime

class SignatureAuthentication(BaseAuthentication):

    SIGNATURE_RE = re.compile(r'^([0-9a-zA-Z]+)\|([0-9a-zA-Z]+)\|([0-9a-zA-Z]+)\|([\d]+)$')
    # ${"JbTm7Y01CeuJxsCO|1234|".concat("JbTm7Y01CeuJxsCO|1234|ViDZmnEO4Q8LCRaR|".concat(timestamp().substring(0, 10)).md5()).concat('|').concat(timestamp().substring(0, 10))}


    KEY_SET = {
        'JbTm7Y01CeuJxsCO': 'ViDZmnEO4Q8LCRaR',
        'nLTqoBUos0USoBrP': 'OiWQWCR08v0ay3PL'
               }

    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').strip()  #  {api_key}|{nonce_str}|{signature}|{timestamp}
        if not auth:
            raise NotAuthenticated('No signature provided')
        match = self.SIGNATURE_RE.search(auth)
        if not match:
            raise AuthenticationFailed('Signature format error')
        api_key = match.group(1)
        nonce_str = match.group(2)
        signature = match.group(3)
        timestamp = int(match.group(4))
        try:
            time_delay = datetime.now() - datetime.fromtimestamp(timestamp)
        except OSError:
            raise AuthenticationFailed('timestamp is invalid')
        if abs(time_delay.seconds) > 60*30:
            raise AuthenticationFailed('request is out of time')
        api_secret = self.KEY_SET.get(api_key)
        if not api_key:
            raise AuthenticationFailed('Api key is error')
        signature_byserver = self.signature_params(api_key, nonce_str, api_secret, timestamp)
        if signature_byserver != signature:
            raise AuthenticationFailed('Signature is error')
        return None

    def signature_params(self, api_key, nonce_str, api_secret, timestamp):
        m = hashlib.md5()
        sign_str = '%s|%s|%s|%d' % (api_key, nonce_str, api_secret, timestamp)
        m.update(sign_str.encode())
        return m.hexdigest()