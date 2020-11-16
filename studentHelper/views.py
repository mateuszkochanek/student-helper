from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Events, Course
from .events.MainPageEvent import MainPageEvent

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
    context = {
        'courses': Course.objects.get_records_by_client_id(request.user.id)
    }
    return render(request, "avg_grade.html", context)


def avg_grade_view_edit_grade(request, pk, grade):
    c = Course.objects.get_record_by_id(pk)
    c.final = grade
    c.save()
    return avg_grade_view(request)
