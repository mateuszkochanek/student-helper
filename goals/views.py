from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *


@login_required(login_url='/login/')
def goals(request):
    goals_not_achieved = []
    goals_achieved = []

    for course in Course.objects.get_records_by_client_id(request.user.id):
        for goal in Goals.objects.get_records_by_course_id(course.pk):
            if goal.achieved == 'N':
                goals_not_achieved.append(goal)
            elif goal.achieved == 'A':
                goals_achieved.append(goal)

    context = {
        'goals_not_achieved': goals_not_achieved,
        'goals_achieved': goals_achieved
    }

    return render(request, "goals.html", context)


@login_required(login_url='/login/')
def new_goal_view(request):
    if request.method == 'POST':
        course = CourseForm(request.POST, client=request.user)
        goal = GoalsForm(request.POST)

        if course.is_valid() and goal.is_valid():
            g = goal.save(commit=False)
            g.course_id = Course.objects.get_record_by_id(course.id)
            g.achieved = 'N'
            g.save()
            return redirect('/goals/')
    else:
        course = CourseForm(client=request.user)
        goal = GoalsForm()

    return render(request, "new_goal.html", {"goals_form": goal, "course_form": course})


@login_required(login_url='/login/')
def new_course_goal(request, pk):
    if request.method == 'POST':
        goal = GoalsForm(request.POST)
        if goal.is_valid():
            g = goal.save(commit=False)
            g.course_id = Course.objects.get_record_by_id(pk)
            g.achieved = 'N'
            g.save()
            return redirect('/course/'+str(pk))
    else:
        goal = GoalsForm()
    return render(request, 'new_course_goal.html', {'goals_form': goal, 'course_id': pk})

