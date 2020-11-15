from .Event import Event


class AvgGradePageEvent(Event):
    def __init__(self, user):
        super(AvgGradePageEvent, self).__init__(user)

    def execute(self):
        pass
