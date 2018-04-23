#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: Pis
@license: Apache Licence 
@software: PyCharm
@file: urls.py
@time: 2018/3/10 16:16
"""
from django.conf.urls import url, include
import xadmin
from django.views.generic import TemplateView

from .views import UserInfoView, UploadImageView, UpdataPwdView, SendEmailCode, MyMessageView
from .views import UpdateEmailView, Mycourse, MyFavCourseView, MyFavTeacherView, MyFavOrgView
urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),  # 个人中心

    url(r'^image/upload/$',  UploadImageView.as_view(), name='image_upload'),
    #个人用户中心修改密码
    url(r'^update/pwd/$', UpdataPwdView.as_view(), name='update_pwd'),
    #发送邮箱验证码
    url(r'^sendemailcode/$', SendEmailCode.as_view(), name='sendemailcode'),
    #修改邮箱
    url(r'^update_email_code/$', UpdateEmailView.as_view(), name='update_email_code'),
    #我的课程
    url(r'^mycourse/$', Mycourse.as_view(), name='mycourse'),
    #我的收藏
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    #我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]
