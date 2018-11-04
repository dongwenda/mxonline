# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse # 指明返回给用户的是什么类型的数据
from django.db.models import Q # 用来查并集

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course
# Create your views here.


class OriView(View):
    """
    课程机构列表页面
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()

        # 热门机构排序
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 机构搜索展示
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) |
                Q(desc__icontains=search_keywords)
            )  # icontain 不区分大小写;Q查并集

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别帅选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 2, request=request)

        orgs = p.page(page)

        # 城市
        all_cities = CityDict.objects.all()
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)   # ModelForm,commit设置为true可以直接保存到库
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错,请填入正确的信息"}',
                                content_type='application/json')

class OrgHomeView(View):
    # 机构首页
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据id获取，机构
        all_courses = course_org.course_set.all()[:3]   # 获取该机构下的课程
        all_teachers = course_org.teacher_set.all()[:1] # 获取该机构下的老师

        # 是否有收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': 'home',
            'has_fav': has_fav
        })


class OrgCourseView(View):
    # 机构课程列表页
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据id获取，机构
        all_courses = course_org.course_set.all()   # 获取该机构下的课程

        # 是否有收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': 'course',
            'has_fav': has_fav
        })


class OrgDescView(View):
    # 机构介绍页
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据id获取，机构

        # 是否有收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': 'desc',
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    # 机构教师列表页
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        # 是否有收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': 'teacher',
            'has_fav': has_fav
        })


class AddFavView(View):
    # 用户收藏,及取消收藏
    def post(self, request):
        if not request.user.is_authenticated():
            #判断用户是否登录
            return HttpResponse('{"status":"fail","msg": "用户未登录"}',
                                content_type='application/json')

        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type) # 里面的user，可以直接传request
        if exist_records:
            # 有已存在的记录，删除收藏
            exist_records.delete()
            return HttpResponse('{"status": "success", "msg": "收藏"}',
                                content_type='application/json')
        else:
            if fav_type > 0 and fav_id > 0 :
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}',
                                    content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏失败，fav_type、fav_id 小于0"}',
                                    content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self, request):
        all_teachers = Teacher.objects.all()

        #热门讲师
        sorted_teacher = all_teachers.order_by("-click_nums")[:3]

        # 教师搜索展示
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) |
                Q(work_company__icontains=search_keywords) |
                Q(position__icontains=search_keywords)
            )  # icontain 不区分大小写;Q查并集

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)

        teacher_nums = all_teachers.count()

        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "sorted_teacher": sorted_teacher,
            "sort": sort,
            "teacher_nums": teacher_nums
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_courses = Course.objects.filter(teacher=teacher)

        # 收藏展示
        has_teacher_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_fav =True
        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_fav = True

        # 讲师排行
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        return render(request, "teacher-detail.html", {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav
        })
