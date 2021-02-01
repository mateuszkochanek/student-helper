from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from studentHelper.models import Course
from .functions import Functions


@login_required(login_url='/login/')
def avg_grade_view(request):
    context = {
        'all_courses': Course.objects.get_records_by_client_id(request.user.id)
    }
    return render(request, "avg_grade.html", context)


@login_required(login_url='/login/')
def avg_grade_calc(request):
    context = {
        'all_courses': Functions().get_courses_and_group_courses(request.user.id),
        'avg': Functions().get_avg(request.user),
    }
    return render(request, "avg_grade.html", context)
