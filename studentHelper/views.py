from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from .models import Events, Description
from .events.UploadCalendarEvent import UploadCalendarEvent
from django.views.generic import ListView, CreateView

from .calendarImport import CalendarImport
from .forms import EventForm, DescriptionForm

# Create your views here.


def main_view(request):
    return render(request, "index.html")


def log_in_view(request):
    return render(request, "login.html")


def calendar_view(request):
    context = UploadCalendarEvent(request.user).execute(0)
    print(context)

    return render(request, "calendar.html", {'d': context}, content_type="text/html")

def new_event_view(request):
    print("HAAAAAAAAALO!!!")
    if request.method == 'POST':
        event = EventForm(request.POST)
        description = DescriptionForm(request.POST)
        print("HAAAAAAAAALO!!!")
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

def avg_grade_view(request):
    return render(request, "avg_grade.html")

def calendar_import(request):
    CalendarImport(request.user)
    return calendar_view(request)

def new_event(request):
    event = EventForm(request.POST)
    description = DescriptionForm(request.POST)
    event.save()
    d = description.save(commit = False)

    d.event_id = event
    d.save()
    return redirect('calendar')
