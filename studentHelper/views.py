from django.shortcuts import render
from django.views.generic.list import ListView
from .events.MainPageEvent import MainPageEvent
from .models import Events, Description, Course
from .events.UploadCalendarEvent import UploadCalendarEvent
from django.views.generic import ListView, CreateView
from .calendarImport import CalendarImport
import threading

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
    context = {
        'courses': Course.objects.get_records_by_client_id(request.user.id)
    }
    return render(request, "avg_grade.html", context)


def avg_grade_view_edit_grade(request, pk, grade):
    c = Course.objects.get_record_by_id(pk)
    c.final = grade
    c.save()
    return avg_grade_view(request)


def calendar_import(request):
    CalendarImport(request.user).start()
    return calendar_view(request)


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
