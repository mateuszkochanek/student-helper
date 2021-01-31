
from django.shortcuts import render, redirect
from datetime import timedelta

from django.views.generic.list import ListView
from .events.MainPageEvent import MainPageEvent
from .models import Events, Description, Course, Teacher
from django.views.generic import ListView, CreateView

import threading
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .tasks import check_if_expired


from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json
# Create your views here.


@login_required(login_url='/login/')
def main_view(request):
    if check_if_expired(request.user.id):
        payload = {"head": "Welcome!", "body": "Hello World",
                "icon": "https://i.imgur.com/dRDxiCQ.png", "url": "https://www.example.com"}
        send_user_notification(user=request.user, payload=payload, ttl=1000)

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
