# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/10/27 22:03'

from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentsView, AddCommentView, VideoPlayView

urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentsView.as_view(), name='course_comments'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^video_play/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play')
]