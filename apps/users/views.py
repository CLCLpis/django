from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect

import json

from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from .forms import UserInfoForm
from .models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            '''
            写入欢迎注册消息
            '''
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册慕雪在线网'
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):

        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:
            for record in records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:  # 链接失效
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "login.html", {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', { 'login_form': login_form})


class LogoutView(View):
    '''
    用户登出
    '''
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse

        return HttpResponseRedirect(reverse('index'))


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            is_register = UserProfile.objects.filter(email=email)
            if is_register:
                send_register_email(email, 'forget')
                return render(request, 'send_success.html')
            else:
                return render(request, 'forgetpwd.html', {'msg': '此账号未注册'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):
    def get(self, request, reset_code):
        records = EmailVerifyRecord.objects.filter(code=reset_code)
        if records:
            for record in records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:  # 链接失效
            return render(request, 'active_fail.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class UserInfoView(LoginRequiredMixin, View):
    '''
    用户个人信息
    '''
    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)

        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure"}', content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''
    def post(self, request):
        # image_form = UploadImageForm(request.POST, request.FILES)
        # if image_form.is_valid():
        #     image = image_form.cleaned_data['image']
        #     request.user.image = image
        #     request.user.save()
        #     pass
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status": "success",}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail",}', content_type='application/json')


class UpdataPwdView(View):
    '''
    在个人中心修改密码
    '''
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            email = request.POST.get('email', '')
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCode(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status": "failure", "msg": "已存在此邮箱"}', content_type='application/json')
        send_register_email(email, 'update')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''
    修改个人邮箱
    '''
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"msg":"验证码出错"}', content_type='application/json')


class Mycourse(LoginRequiredMixin, View):
    '''
    我的课程
    '''
    def get(self, request):
        all_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {'all_courses': all_courses})


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        user_fav_orgs = UserFavorite.objects.filter(fav_type=2, user=request.user)
        for fav_org in user_fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {'user_fav_orgs': org_list,
                                                           })


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        user_fav_teachers = UserFavorite.objects.filter(fav_type=3, user=request.user)
        for fav_teacher in user_fav_teachers:
            teacher_id = fav_teacher.fav_id
            org = Teacher.objects.get(id=teacher_id)
            teacher_list.append(org)
        return render(request, 'usercenter-fav-teacher.html', {'user_fav_teachers': teacher_list})


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        user_fav_courses = UserFavorite.objects.filter(fav_type=1, user=request.user)
        for fav_course in user_fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {'user_fav_courses': course_list,
                                                              })


class MyMessageView(LoginRequiredMixin, View):
    '''我的消息'''
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        """
        清空未读消息
        """
        all_unread_messages = UserMessage.objects.filter(has_read=False, user=request.user.id)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_messages, 3, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {'message': messages})


class IndexView(View):
    '''慕雪在线网首页'''
    def get(self, request):
        '''
        取出轮播图
        :param request:
        :return:
        '''
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs
        })


class LoginUnsafeView(View):
    def get(self, request):
        return render(request, 'login.html',{})

    def post(self,request):
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        import MySQLdb
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='0901', db='mxonline', charset='utf8')
        cursor = conn.cursor()
        sql_select = "select * from users_userprofile where email='{0}' and password='{1}'".format(user_name, make_password(pass_word))
        result = cursor.execute(sql_select)
        for row in cursor.fetchall():
            #查询到用户
            pass
        print('bobby')


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response


def page_error(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response




#     if request.method == 'POST':
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误'})
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})
#

