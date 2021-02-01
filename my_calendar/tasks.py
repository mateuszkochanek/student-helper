from celery import shared_task
from studentHelper.models import Prediction
from django.utils import timezone


@shared_task
def calculate_time(course_id, type):
    data = Prediction.objects.get_record_for_course(course_id, type)
    if data:
        avg = 0
        elements = 0
        for d in data:
            pred_time = d.actual_time
            if pred_time != -1:
                elements += 1
                avg += pred_time
        if elements >= 5:
            return (avg / elements) / 60
    return 0
