from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments
# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        #热门排序
        hot_courses = all_courses.order_by('-click_nums')[:3]

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html',{
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        relate_courses = None
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)

        # 是否有收藏
        is_course_fav = False
        is_org_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course.id, fav_type=1):
                is_course_fav = True
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course.course_org.id, fav_type=2):
                is_org_fav = True

        return render(request, "course-detail.html", {
            'course': course,
            'relate_courses': relate_courses,
            'is_course_fav': is_course_fav,
            'is_org_fav': is_org_fav
        })


class CourseInfoView(View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            'course': course,
            'all_resources': all_resources
        })


class CourseCommentsView(View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course=course)

        return render(request, "course-comment.html", {
            'course': course,
            'all_comments': all_comments
        })


class AddCommentView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            #判断用户是否登录
            return HttpResponse('{"status":"fail","msg": "用户未登录"}',
                                content_type='application/json')

        course_id = int(request.POST.get('course_id', 0))
        comment = request.POST.get('comment', '')
        if course_id > 0 and comment:
            try:
                course = Course.objects.get(id=course_id)  # get方法只会返回一条数据，如果为空或者数据有多就，就会抛异常
            except:
                return HttpResponse('{"status":"fail","msg": "没有该课程"}',
                                    content_type='application/json')
            course_comments = CourseComments()
            course_comments.course = course
            course_comments.user = request.user
            course_comments.commment = comment
            course_comments.save()
            return HttpResponse('{"status":"success","msg": "添加成功"}',
                                content_type='application/json')

        else:
            return HttpResponse('{"status":"fail","msg": "没有该课程，或者评论为空"}',
                                content_type='application/json')