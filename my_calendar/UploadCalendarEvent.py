from studentHelper.models import Events, Description
from django.core.exceptions import EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist
from datetime import date, timedelta
from datetime import datetime
from django.core import serializers
from django.utils import timezone
from collections import defaultdict

class ParsedEvent:

    start_date: str
    end_date: str
    description: str
    size: int

    def __init__(self, start_date, end_date, description, size):
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.size = size


class UploadCalendarEvent():
    def __init__(self, user):
        self.__user = user

    def get_user(self):
        return self.__user

    def execute(self, choose=False, shift="main"):
         # get events from db
         # Gap between times in calendar
         cal_size = 30
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

             for event in events:
                 checked = False
                 extra = Description.objects.get_descriptions(event, choose).first()
                 key = str(event.start_date.weekday())
                 if event.period_type == "ONCE" and extra != None:
                     sd = event.start_date.time()
                     ed = event.end_date.time()
                     size = ((event.end_date - event.start_date).total_seconds())//(60 * cal_size)
                     event_app = ParsedEvent(str(sd), str(ed), str(extra.description), range(int(size)))

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

                     event_app = ParsedEvent(str(""), "Codziennie", str(extra.description), range((cal_size//60) * 24))
                     for i in range(start, end):
                         if str(i) in data:
                             data[str(i)].append(event_app)
                         else:
                             data.update({str(i): [event_app]})


         except(EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist) as e:
             print("e")

         next_shift = start_date.date() + timedelta(days=7)
         prev_shift = start_date.date() - timedelta(days=7)
         period = str(start_date.date()) + " - " + str(end_date.date())
         data.update({"next_shift": str(next_shift)})
         data.update({"prev_shift": str(prev_shift)})
         data.update({"period": period})

         return data
