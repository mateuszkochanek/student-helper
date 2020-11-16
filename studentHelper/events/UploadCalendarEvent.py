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
         data = []
         try:
             events = Events.objects.get_record_by_client_id(self.get_user().id)
             serialized_queryset = serializers.serialize('json', events)
             for event in events:
                 extra = Description.objects.get_descriptions(event).first()
                 key = str(event.start_date.weekday())
                 print(key)

                data.append({
                key : str(event.start_date) + ' ' + str(extra.description)
                 # 'end date': event.end_date,
                 # 'period type': event.period_type,
                 # 'course': extra.course,
                 # 'description': extra.description
                 })

         except(EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist) as e:
             print("e")



         return data
