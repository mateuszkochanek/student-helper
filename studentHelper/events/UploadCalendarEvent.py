from .Event import Event
from studentHelper.models import Events, Description
from django.core.exceptions import EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist
from datetime import date, timedelta
from django.core import serializers
from django.utils import timezone



class UploadCalendarEvent(Event):
    def __init__(self, user):
        super(UploadCalendarEvent, self).__init__(user)

    def execute(self, choose=False):
         # get events from db

         today = date.today()
         day = today.weekday()
         print(day)
         start_date = timezone.now().replace(hour=0, minute=0, second=0) - timedelta(days=day)
         end_date = timezone.now().replace(hour=23, minute=59, second=59) + timedelta(days=(6-day))
         print(start_date)
         print(end_date)
         data = [{} for _ in range(7)]
         try:
             events = Events.objects.get_all_events(self.get_user().id, start_date, end_date)
             #TODO repair this stupid
             # perfectly writed
             # mega code 9

             for event in events:
                 print(event)
                 checked = False
                 print(event.period_type)
                 extra = Description.objects.get_descriptions(event, choose).first()
                 print(extra)
                 key = str(event.start_date.weekday())
                 if event.period_type == "ONCE" and extra != None:
                     for dict in data:
                         if key in dict:
                             dict[key] += '\n' + '\n' + (str(event.start_date.time()) + '-' + str(event.end_date.time())
                                                    + '\n ' + str(extra.description))
                             checked = True
                             break

                     if checked == False:
                         data[event.start_date.weekday()] = {
                                key : str(event.start_date.time()) + '-' + str(event.end_date.time())
                                         + '\n ' + str(extra.description)
                                 }

                 elif event.period_type == "DAILY" and extra != None:
                     for i in range(event.start_date.weekday(), 7):
                        if str(i) in data[i]:
                            data[i][str(i)] += '\n' + '\n' + "Codziennie: " + ' ' + str(extra.description)
                        else:
                            data[i] = { str(i): '\n' + '\n' + "Codziennie: " + ' ' + str(extra.description) }




         except(EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist) as e:
             print("e")



         return data
