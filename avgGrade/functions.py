from studentHelper.models import Course, CourseGroup
from course.finals_update import calc_final


class Functions:
    def __init__(self):
        pass

    def get_avg(self, user):
        courses = self.get_courses_and_group_courses(user)
        for c in courses:
            if self.__is_main_course_in_group(c):
                calc_final(c)
                self.calc_cg_final(c)
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

    def calc_cg_final(self, course):
        all_types = Course.objects.get_all_types_by_id(course.id)
        courses = []
        for c in all_types:
            if CourseGroup.objects.get_records_by_course_id(c):
                courses.append(c)
        minimum = False
        final = 0
        for c in courses:
            cg = CourseGroup.objects.get_records_by_course_id(c)[0]
            final += c.final * cg.weight
            if cg.minimum is True and c.final == 2.0:
                minimum = True
        if final >= 5.25:
            final = 5.5
        elif final >= 4.75:
            final = 5.0
        elif final >= 4.25:
            final = 4.5
        elif final >= 3.75:
            final = 4.0
        elif final > 3.25:
            final = 3.5
        elif final > 2.75:
            final = 3.0
        else:
            final = 2.0
        if minimum:
            course.final = 2.0
            course.save()
        else:
            course.final = final
            course.save()
