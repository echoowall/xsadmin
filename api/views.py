from django.shortcuts import render

# Create your views here.

from .models import *
from django.db.models import Q,F
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.http import Http404,HttpResponseForbidden
from .permissions import *
from .auth import *
from django.core.cache import cache
from api.tasks import update_users_transfer
import logging

logger = logging.getLogger('xsadminloger')

class UserPortView(APIView):
    permission_classes = ( )

    authentication_classes = (SignatureAuthentication, )

    def post(self, request, format=None):
        '''
        用户端口
        :param request:请求对象
        :param format:格式化
        :return:
        '''
        node_id = request.node_id
        node_rate = request.node_rate
        logger.info('node_id=%s,node_rage=%s'%(node_id,node_rate))
        data = request.data
        update_users_transfer.delay(data)
        user_ports_data = cache.get('user_ports_data')

        if user_ports_data is None:
            user_ports_data = User.objects.filter(transfer_enable__gt=F('u')+F('d'), switch=True, is_active=True).values_list('port', 'passwd')
            user_ports_data = list(user_ports_data)
            cache.set('user_ports_data', user_ports_data, timeout= 60)
        return Response(user_ports_data)