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
from django.urls import path, include


from studentHelper.views import main_view, log_in_view
from register.views import register
from studentHelper.views import ( main_view, log_in_view, calendar_view, avg_grade_view,
    calendar_import, new_event_view ) 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name="register"),
    path('', main_view),
    path('', include('django.contrib.auth.urls')),
    path('calendar/', calendar_view),
    path('avgGrade/', avg_grade_view),
    path('calendar/new', new_event_view, name='new'),
    path('calendar_import', calendar_import, name='calendar_import')


]
