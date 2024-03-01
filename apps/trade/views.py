from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer, OrderDetailSerializer
from .models import ShoppingCard, OrderInfo, OrderGoods
import time
from random import Random
from utils.alipay import AliPay
from MXshop.settings import private_key_path, ali_pub_key_path

# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    '''购物车功能
    list:
        获取购物车列表
    create:
        加入购物车
    delete:
        删除购物车
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication, )
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCard.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()


class OrderViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.ReadOnlyModelViewSet):
    '''订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create:
        新增订单
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication, )

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderInfoSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCard.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()   
        return order


class AliPayView(APIView):
    def get(self, request):
        '''
        处理支付宝的return_url
        '''
        processed_dict = {}
        for key, value in request.GET.items:
            processed_dict[key] = value
        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            debug=True,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )
        verify_result = alipay.verify(processed_dict, sign)
        if verify_result is True:
            order_sn = processed_dict.get("out_trade_no", None)
            trade_no = processed_dict.get("trade_no", None)
            trade_status = processed_dict.get("trade_status", None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = timezone.now()
                existed_order.save()

                response = redirect("index")
                response.set_cookie("nextPath", "pay", max_age=2)
                return response
            else:
                response = redirect("index")
                return response

            return Response("success")
            
    def post(self, request):
        '''
        处理支付宝的notify_url
        '''
        processed_dict = {}
        for key, value in request.POST.items:
            processed_dict[key] = value
        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            debug=True,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )
        verify_result = alipay.verify(processed_dict, sign)
        if verify_result is True:
            order_sn = processed_dict.get("out_trade_no", None)
            trade_no = processed_dict.get("trade_no", None)
            trade_status = processed_dict.get("trade_status", None)
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = timezone.now()
                existed_order.save()

            return Response("success")


