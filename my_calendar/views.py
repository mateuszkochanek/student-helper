from django.shortcuts import render, redirect
from .UploadCalendarEvent import UploadCalendarEvent
from .forms import EventForm, DescriptionForm, DescourseForm, CourseForm, TeacherForm
from .calendarImport import CalendarImport
from django.contrib.auth.decorators import login_required
from studentHelper.models import Events, Description


@login_required(login_url='/login/')
def calendar_view(request, shift="main"):
    context = UploadCalendarEvent(request.user).execute(shift=shift)
    return render(request, "my_calendar.html", {'d': context}, content_type="text/html")


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
            return redirect('/calendar/main')
    else:
        event = EventForm()
        description = DescriptionForm()

    return render(request, "new_event.html", {"event_form": event, "description_form": description})


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
            return redirect('/calendar/main')
    else:
        event = EventForm()
        description = DescourseForm()
        course = CourseForm()
        teacher = TeacherForm()

    return render(request, "new_course.html", {"event_form": event, "descourse_form": description,
                                               "course_form": course, "teacher_form": teacher})


@login_required(login_url='/login/')
def scheduler(request, shift="main"):
    context = UploadCalendarEvent(request.user).execute(True, shift=shift)

    return render(request, "scheduler.html", {'d': context}, content_type="text/html")


@login_required(login_url='/login/')
def calendar_import(request):
    if request.method == 'POST' and 'myfile' in request.FILES:
        file = request.FILES['myfile']
        CalendarImport(request.user, file)
    return scheduler(request)

@login_required(login_url='/login/')
def edit_event_view(request, pk):

    my_event = Events.objects.get_record_by_id(pk)
    my_description = my_event.description

    if request.method == 'POST':
        event = EventForm(request.POST, instance=my_event)
        description = DescriptionForm(request.POST, instance=my_description)

        if event.is_valid() and description.is_valid():
            event.save()
            description.save()
            return redirect('/calendar/main')
    else:

        event = EventForm(instance=my_event)
        description = DescriptionForm(instance=my_description)

    return render(request, "new_event.html", {"event_form": event, "description_form": description, "edit": True})
