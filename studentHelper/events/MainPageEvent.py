from .Event import Event


class MainPageEvent(Event):
    def __init__(self, user):
        super(MainPageEvent, self).__init__(user)

    def execute(self):
        pass
