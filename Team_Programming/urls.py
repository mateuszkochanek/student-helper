"""Team_Programming URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, register_converter

from studentHelper.views import *
from my_calendar.views import *
from studentHelper.models import Course
from studentHelper.converts import FloatUrlParameterConverter
from register.views import register
from course.views import *
from avgGrade.views import *
from goals.views import *
from my_statistics.views import *


register_converter(FloatUrlParameterConverter, 'float')


urlpatterns = [
    path('webpush/', include('webpush.urls')),
    path('admin/', admin.site.urls),
    path('register/', register, name="register"),
    path('', main_view, name='main'),
    path('', include('django.contrib.auth.urls')),
    path('calendar/new', new_event_view, name='new'),
    path('calendar/edit/<str:pk>', edit_event_view, name='edit_event'),
    path('calendar/delete/<str:pk>', delete_event_view, name='delete_event'),
    path('calendar/course', new_course_view, name='new_course'),
    path('calendar/<str:shift>', calendar_view, name='calendar'),
    path('scheduler/<str:shift>', scheduler, name='scheduler'),
    path('avgGrade/', avg_grade_view, name='avg_grade_view'),
    path('avgGrade/avg', avg_grade_calc, name='avg_grade_calc'),
    path('calendar_import', calendar_import, name='calendar_import'),
    path('course/<int:pk>', course_view, name='course'),
    path('temp/', temp, name='temp'),
    path('course/<int:pk>/configure-webpage', configure_webpage_view, name='configure_webpage'),
    path('course/<int:pk>/edit', edit_course_view, name='edit_course'),
    path('course/<int:pk>/deleted', delete_course_view, name='delete_course'),
    path('course/<int:pk>/pass_rules', pass_rules_view, name='pass_rules'),
    path('mark/add/<int:pk>', add_mark_view, name='mark_add'),
    path('mark/edit/<int:pk>', edit_mark_view, name='mark_edit'),
    path('temp/', temp, name='temp'),
    path('new_pass_rules/<int:pk>', new_pass_rules, name='new_pass_rules'),
    path('course/<int:pk>/events/<str:desc>/<int:time>', new_course_event_view, name='course_event'),
    path('course/<int:pk>/description', new_course_event_description_view, name='course_e_description'),
    path('goals/', goals, name="goals"),
    path('goals/new/', new_goal_view, name="new_goal"),
    path('goals/delete/<int:pk>', delete_goal, name='delete_goal'),
    path('course/new_goal/<int:pk>', new_course_goal_view, name='new_course_goal'),
    path('course/edit_goal/<int:pk>/<int:cid>', edit_course_goal_view, name='edit_course_goal'),
    path('course/delete/<int:pk>/<int:gid>', delete_course_goal, name='delete_course_goal'),
    path('goals/edit/<int:pk>', edit_goal_view, name='edit_goal'),
    path('statistics/days', statisticsDays, name='statisticsDays'),
    path('statistics/timeSpentOnCourses', statisticsTimeSpentOnCourses, name='statisticsTimeSpentOnCourses'),
    path('statistics/ratios', statisticsRatios, name='statisticsRatios'),
    path('webpush/expired_event/<int:pk>', expired_event_view, name='expired_event'),
    path('course/<int:pk>/file/add/', add_file_view, name='file_add'),
    path('course/files/edit<int:pk>/<str:folder>/<str:file>', edit_files_view, name='edit_file'),
    path('course/files/show/<int:pk>/', show_files_view, name='show_files'),
    path('course/files/delete/<int:pk>/<str:folder>/<str:file>', delete_file_view, name='delete_file'),
    path('course/files/download/<int:pk>/<str:folder>/<str:file>', download_file_view, name='download_file'),
    path('tinymce/', include('tinymce.urls')),
]
