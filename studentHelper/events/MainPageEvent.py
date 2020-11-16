from .Event import Event
from studentHelper.models import Events, Description
from django.core.exceptions import EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist


class MainPageEvent(Event):
    def __init__(self, user):
        super(MainPageEvent, self).__init__(user)

    def execute(self):

        # get events from db
        data = []
        try:
            events = Events.objects.get_record_by_client_id(self.get_user().id)
            for event in events:
                extra = Description.objects.get_descriptions(event).first()
                # key = 'event'+ str(event.id)
                data.append({
                'start date': event.start_date,
                'end date': event.end_date,
                'period type': event.period_type,
                'course': extra.course,
                'description': extra.description
                })
        except(EmptyResultSet, MultipleObjectsReturned, ObjectDoesNotExist):
            pass

        return data
