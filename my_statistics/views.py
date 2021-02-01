from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .helpers import *


@login_required(login_url='/login/')
def statisticsDays(request):
    daysToEndOfSemester = get_days_to_end_of_semester(request.user.id)
    daysInSemester = get_number_of_days_in_semester(request.user.id)
    print('statisticsDays')

    context = {
        'daysToEndOfSemester': daysToEndOfSemester,
        'daysInSemester': daysInSemester,
    }

    return render(request, 'statistics.html', context)


@login_required(login_url='/login/')
def statisticsTimeSpentOnCourses(request):
    courseNames, timeSpendOnCourses = get_times_by_courses(request.user.id)
    print('statisticsTimeSpentOnCourses')

    context = {
        'courseNames': courseNames,
        'timeSpendOnCourses': timeSpendOnCourses
    }

    return render(request, 'statistics.html', context)
