from django.db import models
from datetime import date, timedelta


class TeacherManager(models.Manager):
    """
        Model: Teacher
        Usage: Import model and then use Teacher.objects.[below_options]
    """

    def add_record(self, name, surname, title, webpage):
        """ Add new record to DB

            name: String
            surname: String
            title: String
            webpage: String

        """
        try:
            self.get(name=name, surname=surname, title=title)
        except:
            teacher = self.create(name=name, surname=surname, title=title, webpage=webpage)
            teacher.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_record_by_name_surname_title(self, name, surname, title):

        return self.get(name=name, surname=surname, title=title)


class CourseManager(models.Manager):
    """
        Model: Course
        Usage: Import model and then use Course.objects.[below_options]
    """

    def add_record(self, client, teacher, ECTS, name, type):
        """ Add new record to DB

            client: object of User,
            teacher: object of Teacher
            name: String
            type: 'W', 'C', 'L'

        """
        try:
            self.get(client_id=client, teacher=teacher, name=name, type=type)
        except:
            course = self.create(client_id=client, teacher_id=teacher, ECTS=ECTS,
                        name=name, type=type, final=0)
            course.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_records_by_client_id(self, client_id):
        return self.filter(client_id=client_id)

    def get_main_records_by_client_id(self, client_id):
        all_courses = self.get_records_by_client_id(client_id)
        main_courses = []

        for type in ['W', 'C', 'L']:
            main_courses += [c for c in all_courses if c.type == type]
            for course in main_courses:
                all_courses = [c for c in all_courses if not self.__isTheSameSubject(c, course)]

        return main_courses

    def __isTheSameSubject(self, c1, c2):
        return c1.name == c2.name \
               or c1.name[:-2] == c2.name \
               or c1.name == c2.name[:-2]\
               or c1.name[:-2] == c2.name[:-2]

    def get_all_forms_by_id(self, id):
        main_course = self.get_record_by_id(id)
        return list(self.filter(client_id=main_course.client_id, name=main_course.name)) \
               + list(self.filter(client_id=main_course.client_id, name=main_course.name + 'TN')) \
               + list(self.filter(client_id=main_course.client_id, name=main_course.name + 'TP'))



class ComponentsManager(models.Manager):
    """
        Model: Components
        Usage: Import model and then use Components.objects.[below_options]
    """

    def add_record(self, course, form, weight, type):
        """ Add new record to DB

            course: object of Course,
            form: ACTIV, EXAM, QUIZ, TEST, LIST
            weight: Float
            type: POINT, MARK, PERC

        """

        component = self.create(course_id=course, form=form, weight=weight,
                    type=type)
        component.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_records_by_course_id(self, course_id):
        return self.filter(course_id=course_id)


class ThresholdsManager(models.Manager):
    """
        Model: Thresholds
        Usage: Import model and then use Thresholds.objects.[below_options]
    """

    def add_record(self, course, p_2_0, k_2_0, p_2_5, k_2_5, p_3_0,
                   k_3_0, p_3_5, k_3_5, p_4_0, k_4_0, p_4_5, k_4_5, p_5_0, k_5_0,
                   p_5_5, k_5_5, type):
        """ Add new record to DB

            course: object of Course,

        """

        component = self.create(course_id=course, p_2_0=p_2_0, k_2_0=k_2_0, p_2_5=p_2_5,
                                k_2_5=k_2_5, p_3_0=p_3_0, k_3_0=k_3_0, p_3_5=p_3_5,
                                k_3_5=k_3_5, p_4_0=p_4_0, k_4_0=k_4_0, p_4_5=p_4_5,
                                k_4_5=k_4_5, p_5_0=p_5_0, k_5_0=k_5_0, p_5_5=p_5_5,
                                k_5_5=k_5_5, type=type)
        component.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_records_by_course_id(self, course_id):
        return self.filter(course_id=course_id)


class ModyficationManager(models.Manager):
    """
        Model: Modyfication
        Usage: Import model and then use Modyfication.objects.[below_options]
    """

    def add_record(self, course, mod, val, type):
        """ Add new record to DB

            course: object of Course,

        """

        component = self.create(course_id=course, mod=mod, val=val, type=type)
        component.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_records_by_course_id(self, course_id):
        return self.filter(course_id=course_id)

class CourseGroupManager(models.Manager):
    """
        Model: CourseGroup
        Usage: Import model and then use CourseGroup.objects.[below_options]
    """

    def add_record(self, course, weight, minimum):
        """ Add new record to DB

            course: object of Course,

        """

        component = self.create(course_id=course, weight=weight, minimum=minimum)
        component.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_records_by_course_id(self, course_id):
        return self.filter(course_id=course_id)




class EventsManager(models.Manager):
    """
        Model: Events
        Usage: Import model and then use Events.objects.[below_options]
    """

    def add_record(self, client, start_date, end_date, period_type):
        """ client -> object, current client """

        event = self.create(client_id=client, start_date=start_date,
                            end_date=end_date, period_type=period_type)

        # TODO triggers
        event.save()
        return event

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_record_by_client_id(self, client_id):
        return self.filter(client_id=client_id)

    def get_events(self, client_id, start_date, end_date):
        return self.filter(client_id=client_id,
                           start_date__range=[start_date, end_date],
                           end_date__range=[start_date, end_date]
                           )

    def get_all_events(self, client_id, start_date, end_date):
        q1 = self.filter(client_id=client_id,
                         start_date__range=[start_date, end_date],
                         end_date__range=[start_date, end_date])
        q2 = self.filter(client_id=client_id, start_date__lte=end_date,
                         period_type="DAILY")
        return q1.union(q2)

    def delete_event_by_id(self, id):
        # TODO triggers?
        self.filter(id=id).delete()


class DescriptionManager(models.Manager):
    """
        Model: Description
        Usage: Import model and then use Description.objects.[below_options]
    """

    def add_record(self, event, course, description):
        """ event: object of Event """

        description = self.create(event_id=event, course=course, description=description)
        description.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_descriptions(self, event, course):
        if course:
            return self.filter(event_id=event, course=course).all()
        else:
            return self.filter(event_id=event).all()


class GoalsManager(models.Manager):
    """
        Model: Goals
        Usage: Import model and then use Goals.objects.[below_options]
    """

    def add_record(self, course, end_date, type, description):
        """ course: object of Course"""

        goal = self.create(course_id=course, end_date=end_date,
                           type=type, description=description)
        goal.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_records_by_course_id(self, course_id):
        return self.filter(course_id=course_id)


class FilesManager(models.Manager):
    """
        Model: Files
        Usage: Import model and then use Files.objects.[below_options]
    """

    def add_record(self, course, file_path, description):
        """ course: object of Course """

        file = self.create(course_id=course, file_path=file_path,
                           description=description)
        file.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)


class PredictionManager(models.Manager):
    """
        Model: Prediction
        Usage: Import model and then use Prediction.objects.[below_options]
    """

    def add_record(self, course, start_date, pred_time, actual_time):
        """ course: object of Course """

        prediction = self.create(course_id=course, start_date=start_date,
                                 pred_time=pred_time, actual_time=actual_time)
        prediction.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)


class MarksManager(models.Manager):
    """
        Model: Marks
        Usage: Import model and then use Marks.objects.[below_options]
    """

    def add_record(self, course, mark, mark_type, weight):
        """ course: object of Course """

        prediction = self.create(course_id=course, mark=mark,
                                 mark_type=mark_type, weight=weight)
        prediction.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def getMarks(self, course):
        return self.filter(course_id=course).values('mark', 'mark_type', 'weight')
