from studentHelper.models import Goals, Components, Course, Marks, Thresholds
from django.utils import timezone


def if_pass_rules_exist(course):
    res = True
    if not Components.objects.get_records_by_course_id(course):
        res = False
    return res


def if_activ_in_pass_rules(course):
    res = False
    for c in Components.objects.get_records_by_course_id(course):
        if c.type == 'ACTIV':
            res = True
    return res


def update_goals(user_id):
    courses = Course.objects.get_records_by_client_id(user_id)
    for course in courses:
        goals = Goals.objects.get_records_by_course_id(course)
        for goal in goals:
            if goal.end_date < timezone.now():
                goal.achieved = 'E'
            if goal.type == 'M':
                calc_final(course)
                if course.final >= goal.value:
                    goal.achieved = 'A'
            elif goal.type == 'A':
                marks = Marks.objects.getMarks(course)
                act = 0
                for m in marks:
                    if m['mark_form'] == 'ACTIV':
                        act += m['weight'] * m['mark']
                if act >= goal.value:
                    goal.achieved = 'A'
            goal.save()


def calc_final(course):
    marks = Marks.objects.getMarks(course)
    final = 0
    for m in marks:
        final += m['weight'] * m['mark']

    thresholds = Thresholds.objects.get_records_by_course_id(course)
    thresholds = thresholds[0]
    if final > thresholds.p_5_5:
        final = 5.5
    elif final > thresholds.p_5_0:
        final = 5.0
    elif final > thresholds.p_4_5:
        final = 4.5
    elif final > thresholds.p_4_0:
        final = 4.0
    elif final > thresholds.p_3_5:
        final = 3.5
    elif final > thresholds.p_3_0:
        final = 3.0
    else:
        final = 2.0
    course.final = final
    course.save()
