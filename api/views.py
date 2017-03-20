from django.shortcuts import render

# Create your views here.



from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.http import Http404, HttpResponseForbidden, HttpResponse
from .permissions import *
from .auth import *
from wechatpy.replies import TextReply
import logging
from . import service

logger = logging.getLogger('xsadminloger')

class UserPortView(APIView):
    permission_classes = ( )

    authentication_classes = (SignatureAuthentication, )

    def post(self, request):
        '''
        用户端口
        :param request:请求对象
        :return:
        '''
        node = request.node
        logger.info('node:%s'%(node))
        data = request.data
        logger.info('request:%s',data)
        user_ports_data = service.update_transfer_fetch_users(data, node)
        return Response(user_ports_data)

class WeChatView(APIView):

    permission_classes = ()
    authentication_classes = (WeChatSignatureAuthentication, )

    def get(self, request):
        return HttpResponse(request.GET.get('echostr'))

    def post(self, request):
        msg = parse_message(request.data)
        replay = TextReply(message='test')
        return HttpResponse(replay.render())

