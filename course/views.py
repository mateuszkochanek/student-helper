from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from studentHelper.models import Course, Teacher, Marks, Goals
from studentHelper.views import main_view


@login_required(login_url='/login')
def course_view(request, pk):
    context = {
        'course': Course.objects.get_record_by_id(pk),
        'forms': Course.objects.get_all_forms_by_id(pk),
        'marks': Marks.objects.getMarks(pk),
        'goals': Goals.objects.get_records_by_course_id(pk)
    }

    if context['course'].client_id != request.user:
        return main_view(request)

    return render(request, "course.html", context)


@login_required(login_url='/login')
def temp(request):
    pass
