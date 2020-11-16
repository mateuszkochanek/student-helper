from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Post, Events
from .events.UploadCalendarEvent import UploadCalendarEvent

# Create your views here.


def post_list_view(request):
    post_objects = Post.objects.all()
    context = {
        'post_objects' : post_objects
    }
    return render(request, "posts/index.html", context)


def main_view(request):
    return render(request, "index.html")


def log_in_view(request):
    return render(request, "login.html")


def calendar_view(request):
    context = UploadCalendarEvent(request.user).execute(0)
    print(context)

    return render(request, "calendar.html", {'d': context}, content_type="text/html")


def avg_grade_view(request):
    return render(request, "avg_grade.html")
