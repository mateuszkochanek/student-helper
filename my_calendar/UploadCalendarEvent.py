from studentHelper.models import Events, Description, CourseEvents, Course
from django.core.exceptions import EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist
from datetime import date, timedelta
from datetime import datetime
from django.core import serializers
from django.utils import timezone
from collections import defaultdict

from itertools import chain

class ParsedEvent:

    start_date: str
    day_date: str
    end_date: str
    description: str
    id: int
    size: int


    def __init__(self, start_date, end_date, description, id, size):
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.size = size
        self.id = id


class UploadCalendarEvent():
    def __init__(self, user):
        self.__user = user

    def get_user(self):
        return self.__user


    def get_event(self, event, extra):

        if type(event) == CourseEvents:
            description = event.course_id.course_name + ': '
            description += str(event.description)
        else:
            description = extra.description

        event_app = None
        cal_size = 30

        sd = event.start_date.time()
        ed = event.end_date.time()
        size = ((event.end_date - event.start_date).total_seconds())//(60 * cal_size)
        if event.whole_day == True:
            event_app = ParsedEvent(str(""), "Cały dzień", str(description),
                        event.id, range((cal_size//60) * 24))
        else:
            event_app = ParsedEvent(str(sd), str(ed), str(description),
                        event.id, range(int(size)))

        return event_app

    def execute(self, choose=False, shift="main"):
         # get events from db
         # Gap between times in calendar

         data = {}
         today = date.today()
         day = today.weekday()
         if shift == "main":
             start_date = timezone.now().replace(hour=0, minute=0, second=0) - timedelta(days=day)
             end_date = timezone.now().replace(hour=23, minute=59, second=59) + timedelta(days=(6-day))
         else:
             shift_conv = datetime.strptime(shift, '%Y-%m-%d')
             start_date = timezone.now().replace(year=shift_conv.year, month=shift_conv.month,
                                                 day=shift_conv.day, hour=0, minute=0, second=0)
             end_date = start_date + timedelta(days=6)
         try:
             events = Events.objects.get_all_events(self.get_user().id, start_date, end_date)
             courses = Course.objects.get_records_by_client_id(self.get_user().id)
             course_events = None
             for course in courses:
                 query = CourseEvents.objects.get_all_events(course.id, start_date, end_date)
                 if query:
                     if course_events != None:
                         course_events = course_events.union(query)
                     else:
                         course_events = query

             if course_events != None:
                 result_list = sorted(chain(events, course_events), key=lambda instance: instance.start_date)
             else:
                 result_list = events

             for event in result_list:
                 if type(event) == CourseEvents:
                     extra = event.description
                 else:
                     extra = Description.objects.get_descriptions(event, choose).first()

                 if event.period_type == "ONCE" and extra != None:
                     key = str(event.start_date.weekday())
                     event_app = self.get_event(event, extra)

                     if key in data:
                         data[key].append(event_app)
                     else:
                         data.update({key: [event_app]})

                 elif event.period_type == "DAILY" and extra != None:
                     start = 0
                     end = 0

                     if event.end_date <= end_date and event.start_date >= start_date:
                         start = event.start_date.weekday()
                         end = event.end_date.weekday() + 1

                     elif event.end_date <= end_date and event.start_date < start_date:
                         start = 0
                         end = event.end_date.weekday() + 1

                     elif event.end_date > end_date and event.start_date >= start_date:
                         start = event.start_date.weekday()
                         end = 7
                     else:
                        start = 0
                        end = 7

                     event_app = self.get_event(event, extra)

                     for i in range(start, end):
                         if str(i) in data:
                             data[str(i)].append(event_app)
                         else:
                             data.update({str(i): [event_app]})

                 elif event.period_type == "WEEKLY" and extra != None:

                     event_app = self.get_event(event, extra)
                     key = event.start_date.weekday()
                     if str(key) in data:
                         data[str(key)].append(event_app)
                     else:
                         data.update({str(key): [event_app]})

                 elif event.period_type == "MONTHLY" and extra != None:
                     start_d = start_date.day
                     end_d = end_date.day
                     if start_date.day > end_date.day:
                         start_d = 0

                     if start_d <= event.start_date.day <= end_d:

                         event_app = self.get_event(event, extra)
                         key = end_date.replace(day=event.start_date.day).weekday()
                         if str(key) in data:
                             data[str(key)].append(event_app)
                         else:
                             data.update({str(key): [event_app]})

                 elif event.period_type == "YEARLY" and extra != None:


                     check_date_s = start_date
                     check_date_e = end_date
                     if start_date.year == end_date.year:
                         check_date_s = check_date_s.replace(year=event.start_date.year)
                         check_date_e = check_date_e.replace(year=event.start_date.year)
                     else:
                         check_date_s = check_date_s.replace(year=event.start_date.year - 1)
                         check_date_e = check_date_e.replace(year=event.start_date.year)

                     if (check_date_s <= event.start_date <= check_date_e):
                         event_app = self.get_event(event, extra)
                         key = event.start_date.replace(year=end_date.year).weekday()
                         if str(key) in data:
                             data[str(key)].append(event_app)
                         else:
                             data.update({str(key): [event_app]})

         except(EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist) as e:
             print("e")


         for i in range(7):
             day = start_date.date() + timedelta(days=i)
             key = "day_" + str(i)
             data.update({key: str(day)})

         next_shift = start_date.date() + timedelta(days=7)
         prev_shift = start_date.date() - timedelta(days=7)
         period = str(start_date.date()) + " - " + str(end_date.date())
         data.update({"next_shift": str(next_shift)})
         data.update({"prev_shift": str(prev_shift)})
         return data
