from .Event import Event


class CalcAvgGradeEvent(Event):
    def __init__(self, user):
        super(CalcAvgGradeEvent, self).__init__(user)

    def execute(self):
        pass
