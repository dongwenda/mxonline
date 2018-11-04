# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/10/27 22:03'

from django.conf.urls import url, include

from .views import UserinfoView, UploadImageView, UpdatePwdView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserinfoView.as_view(), name='user_info'),
    url(r'^imageupload/$', UploadImageView.as_view(), name='image_upload'), # 头像上传
    url(r'^updatepwd/$', UpdatePwdView.as_view(), name='update_pwd') # 个人中心修改密码
]