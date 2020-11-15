from .Event import Event


class AddFinalGradeEvent(Event):
    def __init__(self, user):
        super(AddFinalGradeEvent, self).__init__(user)

    def execute(self):
        pass
