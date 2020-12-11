from django.shortcuts import render, redirect

from .UploadCalendarEvent import UploadCalendarEvent
from .forms import EventForm, DescriptionForm, DescourseForm, CourseForm, TeacherForm
from .calendarImport import CalendarImport
from django.contrib.auth.decorators import login_required



@login_required(login_url='/login/')
def calendar_view(request, shift="main"):

    context = UploadCalendarEvent(request.user).execute(shift=shift)
    print(context)
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
            return redirect('/calendar/main')
    else:
        event = EventForm()
        description = DescourseForm()
        course = CourseForm()
        teacher = TeacherForm()

    return render(request, "new_course.html", {"event_form":event, "descourse_form":description,
                                                "course_form":course, "teacher_form":teacher})


@login_required(login_url='/login/')
def scheduler(request, shift="main"):
    context = UploadCalendarEvent(request.user).execute(True, shift=shift)

    return render(request, "scheduler.html", {'d': context}, content_type="text/html")

@login_required(login_url='/login/')
def calendar_import(request):
    CalendarImport(request.user)
    return scheduler(request)
