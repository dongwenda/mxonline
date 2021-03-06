# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/10/20 14:48'

import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse

class LessonInline():
    model = Lesson
    extra = 0

class CourseResourceInline():
    model = CourseResource
    extra = 0

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','click_nums','add_time', 'get_zj_nums', 'go_to']  # 后台展示出来的字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','click_nums','add_time']
    ordering = ['-click_nums']  #默认排序
    readonly_fields = ['click_nums'] # 只读字段
    exclude = ['fav_nums'] # 编辑态不显示   readonly_fields，exclude不能同时
    inlines = [LessonInline, CourseResourceInline]  #在课程里面，也可以添加这两个表，只能一层嵌套
    list_editable = ['degree', 'desc']   # 在列表也可以编辑的字段
    refresh_times = [3, 5]  # 自动刷新时间
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    def queryset(self):
        # 请求，过滤
        qs = super().queryset()
        qs = qs.filter(is_banner=False)
        return qs


    def save_models(self):
        # 在save或者新增，会触发该方法
        # 在保存课程的时候，统计课程机构的数量
        obj = self.new_obj
        obj.save()
        if obj.course_org:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


    # def post(self, request, *args, **kwargs):
    #     if 'excel' in request.FILES:
    #         pass
    #     return super().post(request, args, kwargs)




class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','click_nums','add_time']  # 后台展示出来的字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','click_nums','add_time']
    ordering = ['-click_nums']  #默认排序
    readonly_fields = ['click_nums'] # 只读字段
    exclude = ['fav_nums'] # 编辑态不显示   readonly_fields，exclude不能同时
    inlines = [LessonInline, CourseResourceInline]  #在课程里面，也可以添加这两个表，只能一层嵌套


    def queryset(self):
        # 过滤
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)