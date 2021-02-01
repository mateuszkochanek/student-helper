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
