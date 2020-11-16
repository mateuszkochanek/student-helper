from studentHelper.models import Course


class AddFinalGradeEvent:
    def __init__(self, user):
        self.__user = user

    def execute(self, coursePk, grade):
        if self.__isGradeValid(grade):
            c = Course.objects.get_record_by_id(coursePk)
            c.final = grade
            c.save()

    def __isGradeValid(self, grade):
        return grade in [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]
