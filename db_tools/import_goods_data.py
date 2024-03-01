import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "/..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MXshop.settings")

import django

django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage

from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail['name']
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))  # 本店价格
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""  # 如果不为none就设置为空串
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""   # 封面图取第一个图片的路径就好

    category_name = goods_detail["categorys"][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    # 为什么上一句中不用get而用filter：因为用filter获取不到数据的时候返回的是一个空的数组，并不会抛出异常
    # 用get时，如果查到数据库中没有数据、或者数据库中有两条 都会抛出异常，
    if category:
        goods.category = category[0]
    goods.save()

    # 将图片保存起来，轮播图
    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()
