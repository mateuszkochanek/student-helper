from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Events, Description
from .events.UploadCalendarEvent import UploadCalendarEvent
from django.views.generic import ListView, CreateView

from .calendarImport import CalendarImport

# Create your views here.


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


class EventListView(CreateView):
    """ View for adding event """
    model = Events
    fields = ['start_date', 'end_date', 'period_type']

    def form_valid(self, form):
        form.instance.client_id = self.request.user
        return super().form_valid(form)

class DescriptionListView(CreateView):
    """ View for adding event """
    model = Description
    fields = ['start_date', 'end_date', 'period_type']

    def form_valid(self, form):
        form.instance.client_id = self.request.user
        return super().form_valid(form)

    def calendar_import(request):
        CalendarImport(request.user)
        context = MainPageEvent(request.user).execute()
        print(context)
        return render(request, "calendar.html", {'d': context}, content_type="text/html")
