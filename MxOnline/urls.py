"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView # 处理静态文件
import xadmin   # 换成xadmin后台管理系统
from django.views.static import serve  # 处理静态文件

from users.views import LoginView, RegisterView, ActiveUserVIew, ForgetPwdView, ResetVIew, ModifyPwdView
from organization.views import OriView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls), # 替换成 xadmin
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserVIew.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetVIew.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}), # 配置上传文件的访问处理函数
    url(r'^org/', include('organization.urls', namespace='org')), # 课程机构url配置
    url(r'^course/', include('courses.urls', namespace='course')), # 课程相关url配置
    url(r'^user/', include('users.urls', namespace='user')) # 课程相关url配置
]
