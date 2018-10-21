# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/10/20 14:48'

import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','click_nums','add_time']  # 后台展示出来的字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','click_nums','add_time']

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course__name', 'name']        # 搜索和过滤外键时，字段需要加上__外键
    list_filter = ['course__name', 'name', 'add_time']

class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson__name', 'name', 'add_time']
    list_filter = ['lesson__name', 'name', 'add_time']

class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download','add_time']
    search_fields = ['course__name', 'name', 'download','add_time']
    list_filter = ['course__name', 'name', 'download','add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
