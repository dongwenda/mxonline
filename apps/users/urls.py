# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/10/27 22:03'

from django.conf.urls import url, include

from .views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MymessageView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserinfoView.as_view(), name='user_info'),
    url(r'^imageupload/$', UploadImageView.as_view(), name='image_upload'), # 头像上传
    url(r'^updatepwd/$', UpdatePwdView.as_view(), name='update_pwd'), # 个人中心修改密码
    url(r'^send_emailcode/$', SendEmailCodeView.as_view(), name='send_emailcode'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    url(r'^myfav_org/$', MyFavOrgView.as_view(), name='myfav_org'),
    url(r'^myfav_teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    url(r'^myfav_course/$', MyFavCourseView.as_view(), name='myfav_course'),
    url(r'^mymessage/$', MymessageView.as_view(), name='mymessage')
]