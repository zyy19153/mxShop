from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model
from MXshop.settings import REGEX_MOBILE
from datetime import datetime, timedelta
# from users.models import VerifyCode
from .models import VerifyCode
import time
import re

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''验证手机号码'''

        # 判断手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已存在')

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码非法')

        # 验证发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)

        if VerifyCode.objects.filter(add_time__gt=make_aware(one_minutes_ago), mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送未超过60s')

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4, label="验证码", write_only=True,
    error_messages={
        "blank": "请输入验证码",
        "required": "请输入验证码",
        "max_length": "验证码格式错误",
        "min_length": "验证码格式错误",
        }, help_text="验证码")

    # 验证username是否存在
    username = serializers.CharField(label="用户名", required=True, allow_blank=True, help_text="用户名",
                                    validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")])
    # 设置密文,输入密码的时候只显示点点,看不到密码.  write_only=True设置后不会返回.
    password = serializers.CharField(style={'input_type': 'password'}, label="密码", help_text="密码", write_only=True)

    # 重载serializer的create的方法, 对密码进行设置. 密码保存在数据表的时候不是明文,会被加密
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data.get("username")).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            print(five_minutes_ago)
            print(last_record.add_time)
            if make_aware(five_minutes_ago) > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码不存在")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    '''用户详情序列化类'''

    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")
