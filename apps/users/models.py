from datetime import datetime

from django.db import models
from django.utils import timezone as datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    '''用户'''
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    mobile = models.CharField(max_length=11, verbose_name="电话号码", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("mail",u"男"),("femail",u"女")), default="femail", verbose_name="性别")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    '''短信验证码'''
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话号码")
    add_time = models.DateTimeField(auto_now=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
