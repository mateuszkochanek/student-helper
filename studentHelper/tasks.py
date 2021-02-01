from celery import shared_task
from .models import CourseEvents
from django.utils import timezone
from .models import CourseEvents, Course
import threading
from webpush import send_user_notification

class ExpiredTasks(threading.Thread):

    def __init__(self, user):
        threading.Thread.__init__(self)
        self.user = user

    def check_if_expired(self):
        courses = Course.objects.get_records_by_client_id(self.user.id)
        if courses:
            for course in courses:
                event = CourseEvents.objects.filter(course_id=course, end_date__lt=timezone.now())
                if event:
                    return event[:1][0].id
        return -1

    def send_notification(self):
        id = self.check_if_expired()
        print(id)
        if id != -1:
            payload = {"head": "Wydarzenia", "body": "Istnieją zakończone wydzrzenia! \n Kliknij aby uzupełnić",
                    "icon": "", "url": "expired_event/" + str(id)}
            send_user_notification(user=self.user, payload=payload, ttl=10000)



# CELERY
# @shared_task
# def check_if_expired(self, user_id):
#     courses = Course.objects.get_records_by_client_id(user_id)
#     if courses:
#         for course in courses:
#             event = CourseEvents.objects.filter(course_id=course, end_date__lt=timezone.now())
#             if event:
#                 return event[:1][0].id
#     return -1
