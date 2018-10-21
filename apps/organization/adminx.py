# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/10/20 14:48'

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']

class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name', 'desc', 'click_nums','fav_nums','image','address','city__name','add_time']
    list_filter = ['name', 'desc', 'click_nums','fav_nums','image','address','city__name','add_time']

class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years','work_company','position','points','click_nums','fav_nums']
    search_fields = ['org__name', 'work_years','work_company','position','points','click_nums','fav_nums']
    list_filter = ['org__name', 'work_years','work_company','position','points','click_nums','fav_nums']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
