from django.shortcuts import render, redirect
from .UploadCalendarEvent import UploadCalendarEvent
from .forms import *
from .calendarImport import CalendarImport
from .tasks import calculate_time
from django.contrib.auth.decorators import login_required
from studentHelper.models import Events, Description, Course, CourseEvents, Prediction



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
def new_course_event_view(request, pk, desc, time):
    print(time)
    if request.method == 'POST':
        event = CourseEventForm(request.POST, desc=desc)
        if event.is_valid():
            e = event.save(commit=False)
            e.course_id = Course.objects.get_record_by_id(pk)
            delta = e.end_date - e.start_date
            e.description = desc
            Prediction.objects.add_record(e.description, e.course_id, e.start_date, delta.total_seconds(), -1)
            e.save()
            return redirect('/calendar/main')
    else:
        event = CourseEventForm(desc=desc)

    return render(request, "new_event_2.html", {"event_form": event, "time":time})



@login_required(login_url='/login/')
def new_course_event_description_view(request, pk):
    if request.method == 'POST':
        description = PredTimeForm(request.POST)
        if description.is_valid():
            desc = description.save()
            time = int(calculate_time(pk, desc))
            return redirect("/course/"+str(pk)+"/events/"+desc+"/"+str(time))
    else:
        description = PredTimeForm()

    return render(request, "new_event.html", {"event_form": description})


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
def delete_event_view(request, pk):
    if pk[0] == 'c':
        pk = pk[1:]
        CourseEvents.objects.delete_event_by_id(int(pk))
    else:
        Events.objects.delete_event_by_id(int(pk))

    return redirect('/calendar/main')

@login_required(login_url='/login/')
def edit_event_view(request, pk):
    if pk[0] != 'c':
        pk = int(pk)
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

        return render(request, "new_event.html",
                    {"event_form": event,
                     "description_form": description,
                     "edit": True,
                     "date": my_event.start_date.date(),
                     "pk": str(pk),
                     })
    else:
        pk = pk[1:]
        pk = int(pk)
        description = ""
        my_event = CourseEvents.objects.get_record_by_id(pk)

        if request.method == 'POST':
            event = CourseEventForm(request.POST, instance=my_event)

            if event.is_valid():
                event.save()
                return redirect('/calendar/main')
        else:
            event = CourseEventForm(instance=my_event)


        return render(request, "new_event.html",
                    {"event_form": event,
                     "description_form": description,
                     "edit": True,
                     "date": my_event.start_date.date(),
                     "pk": 'c' + str(pk),
                     })

@login_required(login_url='/login/')
def expired_event_view(request, pk):
    event = CourseEvents.objects.get_record_by_id(pk)
    if request.method == 'POST':
        pred = PredictionForm(request.POST)
        if pred.is_valid():
            delta = event.end_date - event.start_date
            prediction = Prediction.objects.get_record_by_event(event.course_id, event.start_date, delta.total_seconds())
            pred.save(prediction)
            CourseEvents.objects.delete_event_by_id(pk)
            return redirect('/')
    else:
        pred = PredictionForm()

    return render(request, "expired_event.html", {"pred_form": pred, "event": event})
