from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q # 用来查并集

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utlis.mixin_utils import LoginRequireMixin
# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        #热门排序
        hot_courses = all_courses.order_by('-click_nums')[:3]

        # 课程搜索展示
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords)|
                Q(desc__icontains=search_keywords)|
                Q(detail__icontains=search_keywords)
            ) # icontain 不区分大小写;Q查并集

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


class CourseInfoView(LoginRequireMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        all_resources = CourseResource.objects.filter(course=course)

        # 查询用户是否关联了该课程，如果没有则关联
        has_learn = UserCourse.objects.filter(user=request.user, course=course)
        if not has_learn:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学过该课程的人还学过
        user_courses = UserCourse.objects.filter(course=course)     # 查询course 的所有UserCourse记录
        user_ids = [user_course.user.id for user_course in user_courses]    # 所有用户的id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 所有用户id 的课程
        course_ids = {user_course.course.id for user_course in all_user_courses}   # 课程id
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        return render(request, "course-video.html", {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses
        })


class CourseCommentsView(LoginRequireMixin, View):
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


class VideoPlayView(View):
    """
    视频播放页面
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        all_resources = CourseResource.objects.filter(course=course)

        # 查询用户是否关联了该课程，如果没有则关联
        has_learn = UserCourse.objects.filter(user=request.user, course=course)
        if not has_learn:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学过该课程的人还学过
        user_courses = UserCourse.objects.filter(
            course=course)  # 查询course 的所有UserCourse记录
        user_ids = [user_course.user.id for user_course in
                    user_courses]  # 所有用户的id
        all_user_courses = UserCourse.objects.filter(
            user_id__in=user_ids)  # 所有用户id 的课程
        course_ids = {user_course.course.id for user_course in
                      all_user_courses}  # 课程id
        relate_courses = Course.objects.filter(id__in=course_ids).order_by(
            "-click_nums")[:5]

        return render(request, "course-play.html", {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video
        })