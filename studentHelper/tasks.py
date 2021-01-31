from celery import shared_task
from .models import CourseEvents
from django.utils import timezone


@shared_task
def check_if_expired(user_id):
    print(user_id)
    return True
