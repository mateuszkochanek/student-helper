from .Event import Event


class ImportCalendarEvent(Event):
    def __init__(self, user):
        super(ImportCalendarEvent, self).__init__(user)

    def execute(self):
        pass
