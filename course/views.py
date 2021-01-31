from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms import formset_factory

from studentHelper.models import Course, Teacher, Marks, Goals, Components, Thresholds, Modyfication, Events, CourseEvents
from course.forms import WebPageForm, ThresholdsForm
from studentHelper.views import main_view
from my_calendar.forms import CourseForm, TeacherForm

from .forms import MarkForm, RulesForm, CourseGroupForm
from .files import *
from .websites import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from webpush import send_user_notification


@login_required(login_url='/login')
def course_view(request, pk):
    TYPES = {
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

    teacher = course.teacher_id
    if teacher.webpage != "":
        web = WebsiteMonitoring(course.teacher_id.webpage, request, pk, teacher.id, course)
        web.check_changes()

    context = {
        'course': course,
        'lecture': Course.objects.get_subject_of_type_and_name(course, 'W'),
        'tutorial': Course.objects.get_subject_of_type_and_name(course, 'C'),
        'laboratory': Course.objects.get_subject_of_type_and_name(course, 'L'),
        'marks': Marks.objects.getMarks(pk),
        'goals': Goals.objects.get_records_by_course_id(pk),
        'next_courses': Events.objects.get_next_courses(request.user.id, course.course_name, 3),
        'courseEvents': CourseEvents.objects.get_next_events(course.id, 3)
    }

    # TODO czy da się inaczej?
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
        teacher_form = WebPageForm(request.POST)

        if teacher_form.is_valid():
            t = teacher_form.save(commit=False)
            course.teacher_id.webpage = t.webpage
            course.teacher_id.save()
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, '
                                     'like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get(course.teacher_id.webpage, headers=headers)
            html = r.text
            course.teacher_id.html = html
            course.teacher_id.save()
            teacher_id = course.teacher_id.id
            web = WebsiteMonitoring(course.teacher_id.webpage, request, pk, teacher_id, course)
            web.add_list()
            return redirect('/course/' + str(pk))
    else:
        teacher_form = WebPageForm(request.POST)
    return render(request, "course/configure-webpage.html", {"teacher_form": teacher_form, "course": course})


@login_required(login_url='/login')
def add_file_view(request, pk):

    gds = GoogleDriveStorage()
    f = 'inne'  # uzytkownik wybiera do jakiego fodleru dodac plik (listy/notatki/brudnopis/inne)
    path = '/home/paula/Pulpit/SrodowiskoProgramisty/l4/script.sh'  # uzytkownik wskazuje plik w eksploratorze plikow
    splited = gds.split_path(path)
    file_name = splited[-1]

    user_id = request.user.id
    folder = str(user_id) + '/' + str(pk) + '/' + f
    # gds.get_or_create_folder(folder)

    """
    1. DODANIE PLIKU ZE SCIEZKI path NA DYSK DO FOLDERU folder
    name = '/' + folder + '/' + file_name
    gds.save(name, open(path, 'rb'), path)
    """

    """
    2. WYSWIETLENIE ZAWARTOSCI FOLDERU /
    (directories, files) = gds.listdir("/")
    print(directories)
    print(files)
    """

    """
    3. POBRANIE PLIKU 1.sh DO FOLDERU POBRANE NA KOMPUTERZE
    file_name = 'script.sh'
    path = ''
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        path = location
        path += '\\' + file_name
    else:
        path = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
        path += '/' + file_name
    print(gds.open(u'/2/22/inne/script.sh', path))
    """

    """
    4. WYSWIETLENIE PLIKU ZE SCIEZKI file_path
    file_path = '/home/paula/Pobrane/script.sh'
    wrapper = FileWrapper(open(file_path, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    return response
    """

    """
    5. USUNIECIE PLIKU 1.txt Z FOLDERU test4
    gds.delete('/test4/1.txt')
    """

    # file_name pełna ścieżka
    # print(gds.save("/test4/apps.py", open(file_name, 'rb'), file_name))
    # print(gds.get_or_create_folder('test4/folder'))
    # print(gds.check_file_exists('test4'))
    # print(gds.url('/test4/apps.py'))
    # print(gds.open(u'/test4/apps.py', only_name[-1]))
    # print(gds.open(u'/test4/apps.py', '/home/paula/PycharmProjects/student-helper2/my_calendar/a.py')) doda pod ta 2 sciezka
    return redirect('/course/' + str(pk), {"message": True})


@login_required(login_url='/login')
def add_mark_view(request, pk):
    p = Components.objects.get_records_by_course_id(pk)
    if (p.exists()):
        if request.method == 'POST':
            mark = MarkForm(request.POST, course_id=pk)

            if mark.is_valid():
                m = mark.save(commit=False)
                m.course_id = Course.objects.get_record_by_id(pk)
                m.save()
                return redirect('/course/' + str(pk))
        else:
            mark = MarkForm(course_id=pk)

        return render(request, "new_mark.html", {"mark_form": mark, "pk": pk})

    else:
        # TODO informacja o istniejących zasadach zaliczenia
        return redirect('/course/' + str(pk), {"message": True})


@login_required(login_url='/login')
def edit_mark_view(request, pk):
    my_mark = Marks.objects.get_record_by_id(pk)
    course_id = my_mark.course_id.id

    if request.method == 'POST':
        mark = MarkForm(request.POST, instance=my_mark, course_id=course_id)

        if mark.is_valid():
            mark.save()
            return redirect('/course/' + str(course_id))
    else:
        # TODO info?
        mark = MarkForm(instance=my_mark, course_id=course_id)

    return render(request, "new_mark.html", {"mark_form": mark, "pk": course_id, "edit": True})


@login_required(login_url='/login')
def edit_course_view(request, pk):
    c_course = Course.objects.get_record_by_id(pk)
    c_teacher = c_course.teacher_id

    if request.method == 'POST':
        course = CourseForm(request.POST, instance=c_course)
        teacher = TeacherForm(request.POST, instance=c_teacher)

        if course.is_valid() and teacher.is_valid():
            course.save()
            teacher.save()
            return redirect('/course/' + str(pk))
    else:
        course = CourseForm(instance=c_course)
        teacher = TeacherForm(instance=c_teacher)

    return render(request, "new_course.html", {"course_form": course, "event_form": teacher, "edit": True, "pk": pk})


@login_required(login_url='/login/')
def new_pass_rules(request, pk):
    course = Course.objects.get_record_by_id(pk)
    cg = None
    c = Components.objects.get_records_by_course_id(pk)
    if c.exists():
        return redirect('/course/' + str(pk))
    else:
        if request.method == 'POST':
            if course.type == "W":
                cg = CourseGroupForm(request.POST, course_id=pk)
                if cg.is_valid():
                    cg.save()

            rules = RulesForm(request.POST, course_id=pk)
            thresholds = ThresholdsForm(request.POST)

            if rules.is_valid() and thresholds.is_valid():
                rules.save()
                t = thresholds.save(commit=False)
                t.course_id = course
                t.type = Components.objects.get_records_by_course_id(pk)[0].type
                t.save()
                return redirect('/course/' + str(pk))
        else:
            rules = RulesForm(course_id=pk)
            thresholds = ThresholdsForm()
            if course.type == "W":
                cg = CourseGroupForm(course_id=pk)
        return render(request, 'new_pass_rules.html',
                      {'cg_form': cg, 'rules_form': rules, 'thresholds_form': thresholds, "pk": pk})


@login_required(login_url='/login/')
def pass_rules_view(request, pk):
    c = Components.objects.get_records_by_course_id(pk)
    if c.exists():
        course = Course.objects.get_record_by_id(pk)
        t = Thresholds.objects.get(course_id=pk)
        cg = None
        if request.method == 'POST':
            rules = RulesForm(request.POST, course_id=pk)
            thresholds = ThresholdsForm(request.POST, instance=t)
            if course.type == "W":
                cg = CourseGroupForm(request.POST, course_id=pk)
                if cg.is_valid():
                    cg.save_edit()

            if rules.is_valid() and thresholds.is_valid():
                rules.save_edit()
                thresholds.save()
                return redirect('/course/' + str(pk))
        else:
            if course.type == "W":
                cg = CourseGroupForm(course_id=pk)
                cg.fill_edit()

            rules = RulesForm(course_id=pk)
            rules.fill_edit()
            thresholds = ThresholdsForm(instance=t)
        return render(request, 'new_pass_rules.html',
                      {'cg_form': cg, 'rules_form': rules, 'thresholds_form': thresholds, "pk": pk, "edit": True})

    else:
        # TODO informacja o nieistniejących zasadach
        return redirect('/course/' + str(pk))


@login_required(login_url='/login/')
def delete_course_view(request, pk):
    Course.objects.delete_course_by_id(pk)
    return main_view(request)
