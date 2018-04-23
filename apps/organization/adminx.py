#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: Pis
@license: Apache Licence 
@software: PyCharm
@file: adminx.py
@time: 2018/2/28 19:28
"""

from .models import CourseOrg, Teacher, CityDict

import xadmin


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
