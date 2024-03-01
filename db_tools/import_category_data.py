# 导入category数据的脚本，将数据保存到数据库中。先导category数据后导goods数据
# 为什么导入数据要写一个.py文件而不是直接使用mysql文件导入呢：这样后期可以更方便的做数据修改和维护。
# 这个文件可以教：独立使用django的model ，django的model是可以独立出来使用的
import os
import sys

# 获取当前脚本文件的路径
pwd = os.path.dirname(os.path.realpath(__file__))
# 将整个项目的根目录加入到python的根搜索路径之下
sys.path.append(pwd + "/..")
# 从manage.py中复制过来下面这一行，设置环境变量保持一致，
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MXshop.settings")

import django

django.setup()

from goods.models import GoodsCategory  # 这行代码不能写在上面文件路径配置的前面，要初始化好django后在写这一行
# all_category = GoodsCategory.objects.all()


from db_tools.data.category_data import row_data

for lev1_cat in row_data:
    lev1_instance = GoodsCategory()
    lev1_instance.code = lev1_cat["code"]
    lev1_instance.name = lev1_cat["name"]
    lev1_instance.category_type = 1
    lev1_instance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_instance = GoodsCategory()
        lev2_instance.code = lev2_cat["code"]
        lev2_instance.name = lev2_cat["name"]
        lev2_instance.category_type = 2
        lev2_instance.parent_category = lev1_instance
        lev2_instance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_instance = GoodsCategory()
            lev3_instance.code = lev3_cat["code"]
            lev3_instance.name = lev3_cat["name"]
            lev3_instance.category_type = 3
            lev3_instance.parent_category = lev2_instance
            lev3_instance.save()
