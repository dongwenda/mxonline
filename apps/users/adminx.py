# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/10/20 11:40'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin   # UserAdmin 是和原生的User注册的

from users.models import EmailVerifyRecord,Banner, UserProfile


class BaseSetting(object):  # 后台设置
    enable_themes = True  # 开启主题功能
    use_bootswatch = True

class GlobalSettings(object): #后台全局设置
    site_title = '后台管理系统'
    site_footer = '在线学习'
    menu_style = 'accordion'    # 收起app下的表

# class UserProfileAdmin(UserAdmin):
#     pass

class EmailVerifyRecordAdmin(object): # 需要继承object # model管理器
    list_display = ['code','email','send_type','send_time'] #后台展示出来的字段
    search_fields = ['code','email','send_type']  #后台添加搜索功能，根据这里面的全部字段，时间不能search
    list_filter = ['code','email','send_type','send_time']  # 后台添加过滤器
    model_icon = 'fa fa-user'  # 替换font awesome  icon

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']  # 后台展示出来的字段
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']

# xadmin.site.unregister(UserProfile)
# xadmin.site.register(UserProfile, UserProfileAdmin) # 注册User到自己的模块下
# from django.contrib.auth.models import User
# xadmin.site.unregister(User)    #不要注册原生的 User
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)  # 注册主题功能
xadmin.site.register(views.CommAdminView, GlobalSettings) # 注册全局信息
