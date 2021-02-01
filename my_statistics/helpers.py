from studentHelper.models import Prediction, Course, Events


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
    print()