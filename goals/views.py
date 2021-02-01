from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .helpers import *


@login_required(login_url='/login/')
def goals(request):
    goals_not_achieved = []
    goals_achieved = []
    goals_expired = []

    update_goals(request.user)

    for course in Course.objects.get_records_by_client_id(request.user.id):
        for goal in Goals.objects.get_records_by_course_id(course.pk):
            if goal.achieved == 'N':
                goals_not_achieved.append(goal)
            elif goal.achieved == 'A':
                goals_achieved.append(goal)
            elif goal.achieved == 'E':
                goals_expired.append(goal)

    context = {
        'goals_not_achieved': goals_not_achieved,
        'goals_achieved': goals_achieved,
        'goals_expired': goals_expired
    }

    return render(request, "goals.html", context)


@login_required(login_url='/login/')
def new_goal_view(request):
    if request.method == 'POST':
        course = CourseForm(request.POST, client=request.user)
        goal = GoalsForm(request.POST)

        if not if_pass_rules_exist(course):
            return redirect('/goals/', {'error': 'Nie wprowadzono zasad zaliczenia danego kursu'})

        if course.is_valid() and goal.is_valid():
            if goal.cleaned_data['type'] == 'aktywność' and not if_activ_in_pass_rules(course):
                return redirect('/goals/', {'error': 'Wprowadzone zasady zaliczenia nie przewidują\
                                                        aktywności na danym kursie'})
            g = goal.save(commit=False)
            c = course.cleaned_data['course']
            g.course_id = Course.objects.get_course_by_name_and_type(c[:-2], c[-1], request.user)
            g.achieved = 'N'
            g.save()
            return redirect('/goals/')
    else:
        course = CourseForm(client=request.user)
        goal = GoalsForm()

    return render(request, "new_goal.html", {"goals_form": goal, "course_form": course})


@login_required(login_url='/login/')
def edit_goal_view(request, pk):
    old_version = Goals.objects.get_record_by_id(pk)
    c = Course.objects.get_record_by_id(old_version.course_id.pk)
    if request.method == 'POST':
        goal = GoalsForm(request.POST, instance=old_version)
        course = CourseForm(request.POST, client=request.user)

        if not if_pass_rules_exist(course):
            return redirect('/goals/', {'error': 'Nie wprowadzono zasad zaliczenia danego kursu'})

        if course.is_valid() and goal.is_valid():
            if goal.cleaned_data['type'] == 'aktywność' and not if_activ_in_pass_rules(course):
                return redirect('/goals/', {'error': 'Wprowadzone zasady zaliczenia nie przewidują\
                                                                        aktywności na danym kursie'})
            g = goal.save(commit=False)
            c = course.cleaned_data['course']
            g.course_id = Course.objects.get_course_by_name_and_type(c[:-2], c[-1], request.user)
            g.achieved = 'N'
            g.save()
            return redirect('/goals/')
    else:
        goal = GoalsForm(instance=old_version)
        course = CourseForm(initial={'course': c.course_name+' '+c.type}, client=request.user)
    return render(request, "new_goal.html", {"goals_form": goal, "course_form": course})


@login_required(login_url='/login/')
def new_course_goal_view(request, pk):
    course = Course.objects.get_record_by_id(pk)
    if not if_pass_rules_exist(course):
        return redirect('/course/' + str(pk), {'error': 'Nie wprowadzono zasad zaliczenia danego kursu'})

    if request.method == 'POST':
        goal = GoalsForm(request.POST)
        if goal.is_valid():
            if goal.cleaned_data['type'] == 'aktywność' and not if_activ_in_pass_rules(course):
                return redirect('/course/' + str(pk), {'error': 'Wprowadzone zasady zaliczenia nie przewidują\
                                                                    aktywności na danym kursie'})
            g = goal.save(commit=False)
            g.course_id = Course.objects.get_record_by_id(pk)
            g.achieved = 'N'
            g.save()
            return redirect('/course/'+str(pk))
    else:
        goal = GoalsForm()
    return render(request, 'new_course_goal.html', {'goals_form': goal, 'course_id': pk})


@login_required(login_url='/login/')
def edit_course_goal_view(request, pk, cid):
    old_version = Goals.objects.get_record_by_id(pk)
    course = Course.objects.get_record_by_id(cid)
    if not if_pass_rules_exist(course):
        return redirect('/course/' + str(pk), {'error': 'Nie wprowadzono zasad zaliczenia danego kursu'})

    if request.method == 'POST':
        goal = GoalsForm(request.POST, instance=old_version)
        if goal.is_valid():
            if goal.cleaned_data['type'] == 'aktywność' and not if_activ_in_pass_rules(course):
                return redirect('/course/' + str(pk), {'error': 'Wprowadzone zasady zaliczenia nie przewidują\
                                                                aktywności na danym kursie'})
            g = goal.save(commit=False)
            g.course_id = Course.objects.get_record_by_id(cid)
            g.achieved = 'N'
            g.save()
            return redirect('/course/'+str(pk))
    else:
        goal = GoalsForm(instance=old_version)
    return render(request, 'new_course_goal.html', {'goals_form': goal, 'course_id': pk})


@login_required(login_url='/login/')
def delete_goal(request, pk):
    Goals.objects.delete_goal_by_id(pk)
    return redirect('/goals/')


@login_required(login_url='/login/')
def delete_course_goal(request, pk, gid):
    Goals.objects.delete_goal_by_id(gid)
    return redirect('/course/'+str(pk))
