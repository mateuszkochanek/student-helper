from django.db import models

class TeacherManager(models.Manager):
    """
        Model: Teacher
        Usage: Import model and then use Teacher.objects.[below_options]
    """

    def add_record(self, name, surname, title, webpage):
        teacher = self.create(name=name, surname=surname, title=title, webpage=webpage)
        teacher.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)


class CourseManager(models.Manager):
    """
        Model: Course
        Usage: Import model and then use Course.objects.[below_options]
    """

    def add_record(self, client, teacher_id, ECTS, name, type):
        """ client -> object, current client """
        course = self.create(client_id=client, teacher_id=teacher_id, ECTS=ECTS,
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

    def add_record(self, course_id, group, lab_elements, exer_elements,
                    lect_elements, lab_weight, exer_weight, lect_weight, formula):

        rule = self.create(course_id=course_id, group=lab_elements,
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

class DescriptionManager(models.Manager):
    """
        Model: Description
        Usage: Import model and then use Description.objects.[below_options]
    """

    def add_record(self, event_id, course, description):
        """ client -> object, current client """
        description = self.create(event_id=event_id, course=course, description=description)
        description.save()

    def get_record_by_id(self, id):
        return self.get(pk=id)

    def get_descriptions(self, event):
        q = self.filter(event_id=event).values('course','description')
        return q
