
from django.shortcuts import render, redirect
from datetime import timedelta

from django.views.generic.list import ListView
from .events.MainPageEvent import MainPageEvent
from .models import Events, Description, Course, Teacher
from .events.UploadCalendarEvent import UploadCalendarEvent
from django.views.generic import ListView, CreateView
from .calendarImport import CalendarImport

from .forms import EventForm, DescriptionForm, DescourseForm, CourseForm, TeacherForm

from .avg import get_avg
from .events.AddFinalGradeEvent import AddFinalGradeEvent
from .events.AddEctsEvent import AddEctsEvent
import threading
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/login/')
def main_view(request):
    events_today = Events.objects.get_events(
        request.user.id,
        timezone.now(),
        timezone.now().replace(hour=23, minute=59, second=59)
    ).filter(description__course=1).order_by('start_date')[:5]

    next_events = Events.objects.filter(client_id=request.user.id, description__course=0, start_date__gte=timezone.now()).order_by('start_date')[:5]
    context = {
        'events_today': events_today,
        'next_events': next_events
    }
    return render(request, "index.html", context)


@login_required(login_url='/login/')
def log_in_view(request):
    return render(request, "login.html")


@login_required(login_url='/login/')
def calendar_view(request):
    context = UploadCalendarEvent(request.user).execute(0)
    print(context)

    return render(request, "calendar.html", {'d': context}, content_type="text/html")


@login_required(login_url='/login/')
def new_event_view(request):

    if request.method == 'POST':
        event = EventForm(request.POST)
        description = DescriptionForm(request.POST)

        if event.is_valid() and description.is_valid():

            e = event.save(commit=False)
            e.client_id = request.user
            e.save()
            d = description.save(commit=False)
            d.event_id = e
            d.save()
            return redirect('/calendar')
    else:
        event = EventForm()
        description = DescriptionForm()

    return render(request, "new_event.html", {"event_form":event, "description_form":description})

@login_required(login_url='/login/')
def new_course_view(request):

    if request.method == 'POST':
        event = EventForm(request.POST)
        description = DescourseForm(request.POST)
        course = CourseForm(request.POST)
        teacher = TeacherForm(request.POST)

        if event.is_valid() and description.is_valid() and course.is_valid() and teacher.is_valid():

            t = teacher.save()
            c = course.save(commit=False)
            c.client_id = request.user
            c.teacher_id = t
            c.save()

            e = event.save(commit=False)
            e.client_id = request.user
            e.save()
            d = description.save(commit=False)
            d.event_id = e
            d.save()
            return redirect('/calendar')
    else:
        event = EventForm()
        description = DescourseForm()
        course = CourseForm()
        teacher = TeacherForm()

    return render(request, "new_course.html", {"event_form":event, "descourse_form":description,
                                                "course_form":course, "teacher_form":teacher})


@login_required(login_url='/login/')
def avg_grade_view(request):
    context = {
        'courses': Course.objects.get_records_by_client_id(request.user.id)
    }
    return render(request, "avg_grade.html", context)


@login_required(login_url='/login/')
def avg_grade_view_edit_grade(request, pk, grade):
    AddFinalGradeEvent(request.user).execute(pk, grade)
    return avg_grade_view(request)


@login_required(login_url='/login/')
def avg_grade_view_edit_ects(request, pk, ects):
    AddEctsEvent(request.user).execute(pk, ects)
    return avg_grade_view(request)


@login_required(login_url='/login/')
def avg_grade_calc(request):
    context = {
        'courses': Course.objects.get_records_by_client_id(request.user.id),
        'avg': get_avg(request.user)
    }
    return render(request, "avg_grade.html", context)


@login_required(login_url='/login/')
def calendar_import(request):
    CalendarImport(request.user)
    return scheduler(request)


@login_required(login_url='/login/')
def scheduler(request):
    context = UploadCalendarEvent(request.user).execute(True)
    print(context)

    return render(request, "scheduler.html", {'d': context}, content_type="text/html")
