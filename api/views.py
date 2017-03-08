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
        data = request.data
        for key, value in data.items():
            print("端口[%s]上传了(%s)，下载了(%s)" %(key, value[0], value[1]))

        user_ports = User.objects.filter(transfer_enable__gt=F('u')+F('d'), switch=True, is_active=True).values_list('port', 'passwd')
        #serializer = UserPortSerializer(user_ports, many=True)
        #return Response(serializer.data)
        return Response(user_ports)