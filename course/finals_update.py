from studentHelper.models import Course, Marks, Thresholds


def update_finals(user_id):
    courses = Course.objects.get_records_by_client_id(user_id)
    for course in courses:
        calc_final(course)


def calc_final(course):
    marks = Marks.objects.getMarks(course)
    final = 0
    for m in marks:
        final += m['weight'] * m['mark']

    thresholds = Thresholds.objects.get_records_by_course_id(course)
    if not thresholds:
        return 0
    thresholds = thresholds[0]
    if final >= thresholds.p_5_5:
        final = 5.5
    elif final >= thresholds.p_5_0:
        final = 5.0
    elif final >= thresholds.p_4_5:
        final = 4.5
    elif final >= thresholds.p_4_0:
        final = 4.0
    elif final >= thresholds.p_3_5:
        final = 3.5
    elif final >= thresholds.p_3_0:
        final = 3.0
    else:
        final = 2.0
    course.final = final
    course.save()
