#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: Pis
@license: Apache Licence 
@software: PyCharm
@file: urls.py
@time: 2018/3/7 10:56
"""
from django.conf.urls import url, include
import xadmin
from django.views.generic import TemplateView

from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentView, VideoPlayView

urlpatterns = [
    #课程列表页
               url(r'^list/$', CourseListView.as_view(), name='course_list'),
    #课程详情页
               url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    #章节信息
               url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    #课程评论
               url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name='course_comment'),
    #添加评论
               url(r'^add_comment/$', AddCommentView.as_view(), name='add_course_comment'),

               url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),
]