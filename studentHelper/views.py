
from django.shortcuts import render, redirect
from datetime import timedelta

from django.views.generic.list import ListView
from .events.MainPageEvent import MainPageEvent
from .models import Events, Description, Course, Teacher
from django.views.generic import ListView, CreateView

import threading
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/login/')
def main_view(request):
    events_today = Events.objects.filter(
        client_id=request.user.id,
        description__course=1,
        start_date__gte=timezone.now().replace(hour=00, minute=00, second=1),
        end_date__gte=timezone.now(),
        end_date__lte=timezone.now().replace(hour=23, minute=59, second=59)
    ).order_by('start_date')[:5]

    next_events = Events.objects.filter(
        client_id=request.user.id,
        description__course=0,
        start_date__gte=timezone.now()
    ).order_by('start_date')[:5]

    courses = Course.objects.get_main_records_by_client_id(request.user.id)

    context = {
        'events_today': events_today,
        'next_events': next_events,
        'courses': courses
    }
    return render(request, "index.html", context)


@login_required(login_url='/login/')
def log_in_view(request):
    return render(request, "login.html")
