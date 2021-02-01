from studentHelper.models import Prediction, Course, Events, Components
from django.db.models import Max


def get_times_by_courses(client_id):
    courses = Course.objects.get_records_by_client_id(client_id)
    course_names = []
    times = []
    for course in courses:
        time = 0
        predictions = Prediction.objects.get_records_by_course_id(course)
        for p in predictions:
            if p.actual_time != '':
                time += p.actual_time
        course_names.append(course.course_name)
        times.append(time)
    return course_names, times


def get_end_of_semester(client_id):
    classes = Events.objects.get_classes_by_client_id(client_id)
    return classes.aggregate(Max('end_date'))['end_date__max']


def get_ratios_by_courses(client_id):
    courses = Course.objects.get_records_by_client_id(client_id)
    course_names = []
    ratios = []
    for course in courses:
        actual = 0
        estimated = 0
        predictions = Prediction.objects.get_records_by_course_id(course)
        for p in predictions:
            if p.actual_time != '':
                actual += p.actual_time
                estimated += p.pred_time
        if actual != 0:
            ratios.append(estimated/actual)
            course_names.append(course.course_name)
    return course_names, ratios


def get_times_by_course_and_form(course_id):
    components = Components.objects.get_records_by_course_id(course_id)
    forms = []
    times = []
    for c in components:
        predictions = Prediction.objects.get_record_course_and_form(course_id, c.form)
        time = 0
        for p in predictions:
            if p.actual_time != '':
                time += p.actual_time
        forms.append(c.form)
        times.append(time)
    return forms, times
