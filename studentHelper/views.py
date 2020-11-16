from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Events
from .events.MainPageEvent import MainPageEvent

from .calendarImport import CalendarImport

# Create your views here.


def main_view(request):
    return render(request, "index.html")


def log_in_view(request):
    return render(request, "login.html")


def calendar_view(request):
    context = MainPageEvent(request.user).execute()
    print(context)
    return render(request, "calendar.html", {'d': context}, content_type="text/html")


def avg_grade_view(request):
    return render(request, "avg_grade.html")

def calendar_import(request):
    CalendarImport(request.user)
    context = MainPageEvent(request.user).execute()
    print(context)
    return render(request, "calendar.html", {'d': context}, content_type="text/html")

