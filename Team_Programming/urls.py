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


register_converter(FloatUrlParameterConverter, 'float')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name="register"),
    path('', main_view),
    path('', include('django.contrib.auth.urls')),
    path('calendar/new', new_event_view, name='new'),
    path('calendar/course', new_course_view, name='new_course'),
    path('calendar/<str:shift>', calendar_view, name='calendar'),
    path('scheduler/<str:shift>', scheduler, name='scheduler'),
    path('avgGrade/', avg_grade_view),
    path('avgGrade', avg_grade_calc, name='avg_grade_calc'),
    path('avgGrade/grade/<int:pk>/<float:grade>/', avg_grade_view_edit_grade, name="AvgGradeEditGrade"),
    path('avgGrade/ects/<int:pk>/<int:ects>/', avg_grade_view_edit_ects, name="AvgGradeEditEcts"),
    path('calendar_import', calendar_import, name='calendar_import'),
    path('course/<int:pk>', course_view, name='course'),
    path('mark/add/<int:pk>', add_mark_view, name='mark_add'),
    path('mark/edit/<int:pk>', edit_mark_view, name='mark_edit'),
    path('temp/', temp, name='temp')
]
