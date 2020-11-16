from .Event import Event
from studentHelper.models import Events, Description
from django.core.exceptions import EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist
from datetime import date, timedelta
from django.core import serializers



class UploadCalendarEvent(Event):
    def __init__(self, user):
        super(UploadCalendarEvent, self).__init__(user)

    def execute(self, choose):
         # get events from db

         today = date.today()
         day = today.weekday()

         start_date = today - timedelta(days=day)
         end_date = today + timedelta(days=(6-day))
         data = [{} for _ in range(7)]
         try:
             events = Events.objects.get_record_by_client_id(self.get_user().id)
             #TODO repair this stupid
             # perfectly writed
             # mega code 9
             for event in events:
                 checked = False
                 extra = Description.objects.get_descriptions(event).first()
                 key = str(event.start_date.weekday())
                 if event.period_type == "ONCE":
                     for dict in data:
                         if key in dict:
                             dict[key] += '\n' + '\n' + (str(event.start_date.time()) + '-' + str(event.end_date.time())
                                                    + ' ' + str(extra.description))
                             checked = True
                             break

                     if checked == False:
                         data[event.start_date.weekday()] = {
                                key : str(event.start_date.time()) + '-' + str(event.end_date.time())
                                         + ' ' + str(extra.description)
                                 # 'end date': event.end_date,
                                 # 'period type': event.period_type,
                                 # 'course': extra.course,
                                 # 'description': extra.description
                                 }
                 elif event.period_type == "DAILY" :
                     for i in range(7):
                        if str(i) in data[i]:
                            data[i][str(i)] += '\n' + '\n' + (str(event.start_date.time()) + ' ' + str(extra.description))
                        else:
                            data[i] = { str(i): '\n' + '\n' + (str(event.start_date.time()) + ' ' + str(extra.description)) }




         except(EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist) as e:
             print("e")



         return data
