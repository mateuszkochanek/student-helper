from .models import Course


def get_avg(user):
    courses = Course.objects.get_records_by_client_id(user)
    marks_sum = 0
    ects_sum = 0
    for c in courses:
        if c.final is not None and c.final > 0:
            marks_sum += c.final * c.ECTS
            ects_sum += c.ECTS

    if ects_sum == 0:
        return -1
    return marks_sum/ects_sum