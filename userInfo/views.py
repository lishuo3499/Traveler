from userInfo.models import *
from django.shortcuts import render,HttpResponse,redirect
from api.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from userInfo.serializers import *
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate, login, logout  # 用户
from django.http import HttpResponse, JsonResponse
import urllib.request
from django.contrib.auth.decorators import login_required  # 权限控制
import random  # 随机数
import urllib.request


@api_view(["GET"])
def my_center_data(request):
    user_id = request.GET.get("id")
    user = 1
    fav_num = len(Video_Fav_user.objects.filter(user_id=user_id)) # 获赞数量;
    fensi = len(Friends.objects.filter(my_friend = user_id))    #粉丝数量
    atten_num = len(Friends.objects.filter(self_user = user_id))    #我的关注
    UserInfo.objects.update(is_fav_num =fav_num ,attention_num=atten_num,fs_num=fensi)
    # authenticate(username='123456', password='Lsstc123456789')
    if user is not None:
        userserializer = UserInfoSerializer(UserInfo.objects.filter(id=user_id), many=True)
        return Response(userserializer.data,status=status.HTTP_201_CREATED)
    else:
        return HttpResponse('账号密码错误')

class MyPageNumberPagination(PageNumberPagination):
    #每页显示多少个
    page_size = 10
    #默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "size"
    #最大页数不超过10
    max_page_size = 10
    #获取页码数的
    page_query_param = "page"





