# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-11 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180302_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码'), ('updataemail', '更新邮箱')], max_length=10, verbose_name='验证码类型'),
        ),
    ]