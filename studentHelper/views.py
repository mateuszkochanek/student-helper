
from django.shortcuts import render, redirect
from datetime import timedelta

from django.views.generic.list import ListView
from .events.MainPageEvent import MainPageEvent
from .models import Events, Description, Course, Teacher
from django.views.generic import ListView, CreateView

import threading
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .tasks import ExpiredTasks
from webpush import send_user_notification
# Create your views here.


@login_required(login_url='/login/')
def main_view(request):
    # without celery
    thread = ExpiredTasks(request.user)
    id = thread.send_notification()

    # with celery
    #id = check_if_expired.delay(request.user.id).get()
    # if id != -1:
    #     payload = {"head": "Wydarzenia", "body": "Istnieją zakończone wydzrzenia! \n Kliknij aby uzupełnić",
    #             "icon": "", "url": "expired_event/" + str(id)}
    #     send_user_notification(user=request.user, payload=payload, ttl=10000)

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
    context = {
        'events_today': events_today,
        'next_events': next_events,
    }
    return render(request, "index.html", context)

@login_required(login_url='/login/')
def log_in_view(request):
    return render(request, "login.html")
