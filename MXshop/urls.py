"""MXshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.views.static import serve
from MXshop.settings import MEDIA_ROOT

import xadmin
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, IndexCategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet, AliPayView

router = DefaultRouter()
router.register('goods', GoodsListViewSet, basename='goods_list')
router.register('categories', CategoryViewSet)
router.register('codes', SmsCodeViewSet, basename='codes')  # 发送短信验证码的配置
router.register('users', UserViewSet, basename='users')  # 用户注册配置
router.register('userfavs', UserFavViewSet, basename='userfavs')  # 收藏
router.register('messages', LeavingMessageViewSet, basename='messages') # 留言功能
router.register('address', AddressViewSet, basename='address')
router.register('shopcarts', ShoppingCartViewSet, basename='shopcarts')
router.register('orders', OrderViewSet, basename='orders')
router.register('banners', BannerViewSet, basename='banners')   # 轮播图
router.register('indexgoods', IndexCategoryViewSet, basename='indexgoods') # 首页商品系列数据

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', include(router.urls)),
    re_path('media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path('docs/', include_docs_urls(title='慕学生鲜')),   # drf的文档功能
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),  # token认证功能中的url配置，drf自带的token认证模式
    re_path('login/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('alipay/return/', AliPayView.as_view(), name="alipay"),        # 支付宝支付接口
    path('', include('social_django.urls', namespace='social'))         # 第三方登录url
]
