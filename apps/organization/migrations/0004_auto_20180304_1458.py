# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-04 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20180304_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='course_num',
            field=models.IntegerField(default=0, verbose_name='课程数'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='students',
            field=models.IntegerField(default=0, verbose_name='学习人数'),
        ),
    ]
