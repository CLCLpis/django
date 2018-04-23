from django.db import models
from datetime import datetime

from organization.models import CourseOrg, Teacher

from DjangoUeditor.models import UEditorField
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name='课程教师', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述", default='')
    detail = UEditorField(verbose_name='课程详情', width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    degree = models.CharField(verbose_name="难度", max_length=10, choices=(("cj", '初级'), ('zj', "中级"), ('gj', '高级')))
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟）')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图')
    click_nums = models.IntegerField(default=0, verbose_name='课程点击数')
    tag = models.CharField(default='', verbose_name='课程标签', max_length=12)
    category = models.CharField(verbose_name="课程类别", default='qd', max_length=10, choices=(("qd", '前端'), ('hd', "后端"), ('qz', '全栈')))
    you_need_know = models.CharField(verbose_name="课程须知", default='', max_length=500, )
    teacher_tell_you = models.CharField(verbose_name="老师告知", default='', max_length=500, )
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_zj_nums(self):
        #获取课程章节数
        return self.lesson_set.all().count()
    get_zj_nums.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</a>")
    go_to.short_description = '跳转'

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        #获取章节
        return self.lesson_set.all()


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        #获取章节视频
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟）')
    url = models.CharField(max_length=200, verbose_name='访问地址 ', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='资源名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='下载地址', max_length=100)

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = verbose_name



