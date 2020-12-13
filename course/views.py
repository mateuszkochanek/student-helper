from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from studentHelper.models import Course, Teacher, Marks, Goals, Components
from course.forms import TeacherForm
from studentHelper.models import Course, Teacher, Marks, Goals
from studentHelper.views import main_view

from .forms import MarkForm, RulesForm, CourseGroupForm


@login_required(login_url='/login')
def course_view(request, pk):
    TYPES = {
    "PLUS": "+",
    "MINUS": "-",
    "PKT": "pkt",
    "MARK": "ocena",
    "PERC": "%",
    }

    FORMS = {
    "ACTIV": "aktywność",
    "EXAM": "egzamin",
    "QUIZ": "kartkówka",
    "TEST": "kolokwium",
    "LIST": "lista zadań",
    }

    course = Course.objects.get_record_by_id(pk)

    context = {
        'course': course,
        'lecture': Course.objects.get_subject_of_type_and_name(course, 'W'),
        'tutorial': Course.objects.get_subject_of_type_and_name(course, 'C'),
        'laboratory': Course.objects.get_subject_of_type_and_name(course, 'L'),
        'marks': Marks.objects.getMarks(pk),
        'goals': Goals.objects.get_records_by_course_id(pk)
    }

    #TODO czy da się inaczej?
    for el in context['marks']:
        el['mark_type'] = TYPES[el['mark_type']]
        el['mark_form'] = FORMS[el['mark_form']]

    if context['course'].client_id != request.user:
        return main_view(request)

    return render(request, "course.html", context)


@login_required(login_url='/login')
def temp(request):
    return main_view(request)


@login_required(login_url='/login')
def configure_webpage_view(request, pk):
    course = Course.objects.get_record_by_id(pk)
    if request.method == 'POST':
        teacher_form = TeacherForm(request.POST)

        if teacher_form.is_valid():
            t = teacher_form.save(commit=False)
            course.teacher_id.webpage = t.webpage
            course.teacher_id.save()
            print(course.teacher_id.webpage)
            return redirect('/course/'+str(pk))
    else:
        teacher_form = TeacherForm(request.POST)
    return render(request, "course/configure-webpage.html", {"teacher_form": teacher_form, "course": course})


@login_required(login_url='/login')
def add_mark_view(request, pk):

    p = Components.objects.get_records_by_course_id(pk)
    if(p.exists()):
        if request.method == 'POST':
            mark = MarkForm(request.POST, course_id=pk)

            if mark.is_valid():
                m = mark.save(commit=False)
                m.course_id = Course.objects.get_record_by_id(pk)
                m.save()
                return redirect('/course/'+str(pk))
        else:
            mark = MarkForm(course_id=pk)

        return render(request, "new_mark.html", {"mark_form": mark, "pk": pk})

    return redirect('/course/'+str(pk), {"message": True})

@login_required(login_url='/login')
def edit_mark_view(request, pk):
    my_mark = Marks.objects.get_record_by_id(pk)
    course_id = my_mark.course_id.id

    if request.method == 'POST':
        mark = MarkForm(request.POST, instance=my_mark, course_id=course_id)

        if mark.is_valid():
            mark.save()
            return redirect('/course/'+str(course_id))
    else:
        #TODO info?
        mark = MarkForm(instance=my_mark, course_id=course_id)

    return render(request, "new_mark.html", {"mark_form": mark, "pk": course_id, "edit": True })


@login_required(login_url='/login/')
def new_pass_rules(request, pk):
    if request.method == 'POST':
        rules = RulesForm(request.POST, course_id=pk)
        if rules.is_valid():
            rules.save()
            return redirect('/course/'+str(pk))
    else:
        rules = RulesForm(course_id=pk)
    return render(request, 'new_pass_rules.html', {'rules_form': rules, "pk": pk})


@login_required(login_url='/login/')
def new_course_group(request, pk):
    if request.method == 'POST':
        cg = CourseGroupForm(request.POST, course_id=pk)
        if cg.is_valid():
            cg.save()
            return redirect('/new_pass_rules/'+str(pk))
    else:
        cg = CourseGroupForm(course_id=pk)
    return render(request, 'new_course_group.html', {'cg_form': cg, "pk": pk})
