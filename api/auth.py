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
from django.core.cache import cache
from user.utils import refush_node_app_keyset
import logging
from wechatpy import parse_message
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

logger = logging.getLogger('xsadminloger')

class SignatureAuthentication(BaseAuthentication):

    SIGNATURE_RE = re.compile(r'^([0-9a-zA-Z]+)\|([0-9a-zA-Z]+)\|([0-9a-zA-Z]+)\|([\d]+)$')
    # ${"JbTm7Y01CeuJxsCO|1234|".concat("JbTm7Y01CeuJxsCO|1234|ViDZmnEO4Q8LCRaR|".concat(timestamp().substring(0, 10)).md5()).concat('|').concat(timestamp().substring(0, 10))}

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
        node_set = cache.get('node_api_key_set')
        if not node_set:
            #raise AuthenticationFailed('Api key is not set,please notice the admin')
            logger.error('cache do not has node_set, refush_node_app_keyset it')
            node_set = refush_node_app_keyset()
        api_key_value = node_set.get(api_key)
        if not api_key_value:
            raise AuthenticationFailed('Api key is error')
        api_secret = api_key_value[0]
        if not api_secret:
            raise AuthenticationFailed('Api secret is not set,please notice the admin')
        signature_byserver = self.signature_params(api_key, nonce_str, api_secret, timestamp)
        if signature_byserver != signature:
            raise AuthenticationFailed('Signature is error')
        node_id = api_key_value[1]
        node_rate = api_key_value[2]
        node_group_id = api_key_value[3]
        if not node_id or not node_rate or not node_group_id:
            raise AuthenticationFailed('no node_id or node_rate or node_group_id,please notice the admin')
        request.node = {'node_id': node_id, 'node_rate': node_rate, 'node_group_id': node_group_id}
        return None

    def signature_params(self, api_key, nonce_str, api_secret, timestamp):
        m = hashlib.md5()
        sign_str = '%s|%s|%s|%d' % (api_key, nonce_str, api_secret, timestamp)
        m.update(sign_str.encode())
        return m.hexdigest()

class WeChatSignatureAuthentication(BaseAuthentication):
    '''
    微信接口签名验证
    '''
    def authenticate(self, request):
        token = '666xxx'
        try:
            check_signature(token, request.GET.get('signature'), request.GET.get('timestamp'), request.GET.get('nonce'))
        except InvalidSignatureException:
            raise AuthenticationFailed('signature error')
