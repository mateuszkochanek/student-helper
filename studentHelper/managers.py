from django.db import models

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

        teacher = self.create(name=name, surname=surname, title=title, webpage=webpage)
        teacher.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)


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

        course = self.create(client_id=client, teacher_id=teacher, ECTS=ECTS,
                        name=name, type=type)
        course.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_record_by_client_id(self, client_id):
        return self.get(client_id=client_id)

class RulesManager(models.Manager):
    """
        Model: Rules
        Usage: Import model and then use Rules.objects.[below_options]
    """

    def add_record(self, course, group, lab_elements, exer_elements,
                    lect_elements, lab_weight, exer_weight, lect_weight, formula):
        """ course: object of Course """

        rule = self.create(course_id=course, group=lab_elements,
                    exer_elements=exer_elements,lect_elements=webpage,
                    lab_weight=lab_weight, exer_weight=exer_weight,
                    lect_weight=lect_weight, formula=formula)
        rule.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

class EventsManager(models.Manager):
    """
        Model: Events
        Usage: Import model and then use Events.objects.[below_options]
    """

    def add_record(self, client, start_date, end_date, period_type):
        """ client -> object, current client """

        event = self.create(client_id=client, start_date=start_date,
                            end_date=end_date, period_type=period_type)
        event.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_record_by_client_id(self, client_id):
        return self.get(client_id=client_id)

    def delete_event_by_id(self, id):
        #TODO triggers?
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

    def get_descriptions(self, event):
        return self.filter(event_id=event).values('course','description')


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
        return self.filter(event_id=course).values('mark','mark_type', 'weight')
