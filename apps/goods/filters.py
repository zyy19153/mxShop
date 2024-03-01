from django_filters import rest_framework
from django.db.models import Q
# Q对象(django.db.models.Q)可以对关键字参数进行封装，从而更好地应用多个查询。
# 可以组合使用 &（and）,|（or），~（not）操作符，当一个操作符是用于两个Q的对象,它产生一个新的Q对象。

from .models import Goods


class GoodsFilter(rest_framework.FilterSet):
    '''商品过滤类'''

    pricemin = rest_framework.NumberFilter(field_name="shop_price", help_text="最低价格", lookup_expr='gte')
    pricemax = rest_framework.NumberFilter(field_name="shop_price", lookup_expr='lte')
    top_category = rest_framework.NumberFilter(method='top_category_filter')  # 传递top_category_filter这个函数

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value)).order_by('id')   # Q查询

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'top_category', 'is_hot', 'is_new']
