from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from utils.permissions import IsOwnerOrReadOnly
from .models import UserFav, UserLeaveMessage, UserAddress
from .serializer import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
# Create your views here.


class UserFavViewSet(viewsets.ModelViewSet):
    '''
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已收藏
    '''
    serializer_class = UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication, )
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

    def perform_destroy(self, instance):
        instance.delete()
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer


class LeavingMessageViewSet(viewsets.ModelViewSet):
    '''
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    '''
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication, )

    def get_queryset(self):
        return UserLeaveMessage.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    '''收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    '''
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication, )

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)



