from celery import shared_task
from .models import CourseEvents
from django.utils import timezone
from .models import CourseEvents, Course


@shared_task
def check_if_expired(user_id):
    courses = Course.objects.get_records_by_client_id(user_id)
    if courses:
        for course in courses:
            event = CourseEvents.objects.filter(course_id=course, end_date__lt=timezone.now())
            if event:
                return event[:1][0].id
    return -1
