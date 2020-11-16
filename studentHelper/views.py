
from django.shortcuts import render, redirect
from datetime import timedelta

from django.views.generic.list import ListView
from .events.MainPageEvent import MainPageEvent
from .models import Events, Description, Course
from .events.UploadCalendarEvent import UploadCalendarEvent
from django.views.generic import ListView, CreateView
from .calendarImport import CalendarImport

from .forms import EventForm, DescriptionForm

from .avg import get_avg
from .events.AddFinalGradeEvent import AddFinalGradeEvent
import threading
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/login/')
def main_view(request):
    events = Events.objects.get_events_by_datetime(request.user.id, timezone.now(), timezone.now().replace(hour=00, minute=00, second=1) + timedelta(days=1))
    context = {
        'events': events
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
def avg_grade_calc(request):
    context = {
        'courses': Course.objects.get_records_by_client_id(request.user.id),
        'avg': get_avg(request.user)
    }
    return render(request, "avg_grade.html", context)


@login_required(login_url='/login/')
def calendar_import(request):
    CalendarImport(request.user)
    return calendar_view(request)



