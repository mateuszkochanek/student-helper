from studentHelper.models import Course


class AddEctsEvent:
    def __init__(self, user):
        self.__user = user

    def execute(self, coursePk, ects):
        if self.__isEctsValid(ects):
            c = Course.objects.get_record_by_id(coursePk)
            c.ECTS = ects
            c.save()

    def __isEctsValid(self, ects):
        return ects in range(0, 31)
