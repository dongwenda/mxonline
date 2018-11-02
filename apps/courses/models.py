# -*- encoding:utf-8 -*-
from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name='课程教师', null=True, blank=True)
    name = models.CharField(max_length=50,verbose_name='课程名称')
    desc = models.CharField(max_length=300,verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(choices=(('cj','初级'),('zj','中级'),('gj','高级')),max_length=2)
    learn_times = models.IntegerField(default=0,verbose_name='学习时长（分钟数）')
    students = models.IntegerField(default=0,verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name='封面图',max_length=100, null=True, blank=True)
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    category = models.CharField(max_length=10,verbose_name='课程类别', default='后台开发')
    tag = models.CharField(max_length=30,verbose_name='课程标签', default='')
    youneed_know = models.CharField(max_length=300,verbose_name='课程须知', null=True, blank=True)
    teacher_tell = models.CharField(max_length=300,verbose_name='老师告诉你', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_zj_nums(self):
        # 获取指向它的，外键对象，这里返回一个queryset
        return self.lesson_set.count()

    def get_learn_users(self):
        # 获取学习这门课的用户
        return self.usercourse_set.all()[:3]

    def get_course_lesson(self):
        return self.lesson_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')  # 一对多，多对一都是用外键来关联
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名称')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    url = models.CharField(max_length=100, verbose_name='视频链接', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m',verbose_name='资源文件',max_length=100) # 使用FileField 在后台xadmin管理系统中就展示的上传按钮
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
