#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: Pis
@license: Apache Licence 
@software: PyCharm
@file: forms.py
@time: 2018/3/4 22:19
"""
from django import forms
from operation.models import UserAsk

import re

# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=28)
#     phone = forms.CharField(required=True, min_length=5, max_length=50)
#     course_name = forms.CharField(required=True, min_length=11, max_length=11)


class UserAskForm(forms.ModelForm):
    # my_field =forms.CharField(###)
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')

