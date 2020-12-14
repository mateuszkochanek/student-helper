from studentHelper.models import Course, CourseGroup


class Functions:
    def __init__(self):
        pass

    def add_final_grade(self, coursePk, grade):
        if self.__isGradeValid(grade):
            c = Course.objects.get_record_by_id(coursePk)
            c.final = grade
            c.save()

    def __isGradeValid(self, grade):
        return grade in [0.0, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]

    def add_ects(self, coursePk, ects):
        if self.__isEctsValid(ects):
            c = Course.objects.get_record_by_id(coursePk)
            c.ECTS = ects
            c.save()

    def __isEctsValid(self, ects):
        return ects in range(0, 31)

    def get_avg(self, user):
        courses = self.get_courses_and_group_courses(user)
        marks_sum = 0
        ects_sum = 0
        for c in courses:
            if c.final is not None and c.final > 0:
                marks_sum += c.final * c.ECTS
                ects_sum += c.ECTS

        if ects_sum == 0:
            return -1
        return marks_sum / ects_sum

    def get_courses_and_group_courses(self, client_id):
        all_courses = Course.objects.get_records_by_client_id(client_id)
        result = []

        for course in all_courses:
            if self.__is_standalone_course(course) or self.__is_main_course_in_group(course):
                result += [course]

        return result

    def __is_standalone_course(self, course):
        return not CourseGroup.objects.get_records_by_course_id(course.id)

    def __is_main_course_in_group(self, course):
        courses = Course.objects.get_all_types_by_id(course.id)
        if course.type == "W":
            return True
        if course.type == "C" and not any(c.type == "W" for c in courses):
            return True
        if course.type == "L" and not any(c.type == "W" or c.type == "L" for c in courses):
            return True
        return False
