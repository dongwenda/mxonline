# -*- encoding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser  # auth_user表的类

# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name='昵称',default='')
    birthday = models.DateField(verbose_name='生日',null=True,blank=True)
    gender = models.CharField(choices=(('male','男'),('female','女')), default='female',max_length=6 )
    address = models.CharField(max_length=100,default='')
    mobile = models.CharField(max_length=11, null=True,blank=True)
    image = models.ImageField(upload_to='image/%Y/%m',default='image/default.png',max_length=100, null=True,blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name='验证码')   # verbose_name后台表字段名字
    email = models.EmailField(max_length=50,verbose_name='邮箱')
    send_type = models.CharField(choices=(('register','注册'),('forget','找回密码')),max_length=10,verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name='发送时间')  #datetime.now() 括号要去掉，实例化的时间。如果不去掉，是生成表的时间

    class Meta:
        verbose_name = '邮箱验证码'  # 后台表的名字
        verbose_name_plural = verbose_name  # 不设置这个值，就会自动加s

    def __str__(self):
        return '{}({})'.format(self.email,self.code)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图',max_length=100)
    url = models.URLField(verbose_name='访问地址',max_length=200)
    index = models.IntegerField(default=100,verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
