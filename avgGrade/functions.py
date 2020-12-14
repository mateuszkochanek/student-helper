from studentHelper.models import Course, CourseGroup, Marks, Thresholds


class Functions:
    def __init__(self):
        pass

    def add_final_grade(self, coursePk, grade):
        if self.__isGradeValid(grade):
            c = Course.objects.get_record_by_id(coursePk)
            c.final = grade
            c.save()

    def __isGradeValid(self, grade):
        return grade in [0.0, 2.0, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]

    def add_ects(self, coursePk, ects):
        if self.__isEctsValid(ects):
            c = Course.objects.get_record_by_id(coursePk)
            c.ECTS = ects
            c.save()

    def __isEctsValid(self, ects):
        return ects in range(0, 31)

    def get_avg(self, user):
        courses = self.get_courses_and_group_courses(user)
        for c in courses:
            self.calc_final(c)
            if self.__is_main_course_in_group(c):
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

    def calc_final(self, course):
        marks = Marks.objects.getMarks(course)
        final = 0
        for m in marks:
            final += m['weight'] * m['mark']

        thresholds = Thresholds.objects.get_records_by_course_id(course)
        if not thresholds:
            return 0
        thresholds = thresholds[0]
        if final > thresholds.p_5_5:
            final = 5.5
        elif final > thresholds.p_5_0:
            final = 5.0
        elif final > thresholds.p_4_5:
            final = 4.5
        elif final > thresholds.p_4_0:
            final = 4.0
        elif final > thresholds.p_3_5:
            final = 3.5
        elif final > thresholds.p_3_0:
            final = 3.0
        else:
            final = 2.0
        course.final = final
        course.save()

    def calc_cg_final(self, course):
        all_types = Course.objects.get_all_types_by_id(course.id)
        courses = []
        for c in all_types:
            if CourseGroup.objects.get_records_by_course_id(c):
                courses.append(c)
                self.calc_final(c)
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
