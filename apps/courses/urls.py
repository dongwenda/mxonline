# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/10/27 22:03'

from django.conf.urls import url
from .views import CourseListView

urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
]