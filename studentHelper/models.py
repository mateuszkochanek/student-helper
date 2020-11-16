from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse


from studentHelper.managers import TeacherManager
from studentHelper.managers import CourseManager
from studentHelper.managers import RulesManager
from studentHelper.managers import EventsManager
from studentHelper.managers import DescriptionManager
from studentHelper.managers import GoalsManager
from studentHelper.managers import FilesManager
from studentHelper.managers import PredictionManager
from studentHelper.managers import MarksManager


class Teacher(models.Model):

    # pk generated automaticly

    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    webpage = models.CharField(max_length=60)
    objects = TeacherManager()

    class Meta:
        #TODO Indexes ect.
        verbose_name_plural = "Teacher"

class Course(models.Model):

    TYPES = [
    ("W", "lecture"),
    ("C", "exercises"),
    ("L", "laboratory"),
    ]

    # pk generated automaticly

    # foreign keys
    client_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    teacher_id = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
    )

    # columns
    ECTS = models.IntegerField()
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=1, choices=TYPES)
    final = models.IntegerField(blank=True, default=None)
    objects = CourseManager()



class Rules(models.Model):

    course_id = models.OneToOneField(
    Course,
    on_delete = models.CASCADE,
    primary_key=True,
    )


    group = models.BooleanField()
    lab_elements = models.IntegerField(blank=True)
    exer_elements = models.IntegerField(blank=True)
    lect_elements = models.IntegerField(blank=True)
    lab_weight = models.IntegerField(blank=True)
    exer_weight = models.IntegerField(blank=True)
    lect_weight = models.IntegerField(blank=True)
    formula = models.CharField(max_length=30)
    objects = RulesManager()




class Goals(models.Model):

    TYPES = [
    ("A", "activity"),
    ("M", "marks"),
    ("O", "others"),
    ]

    # pk generated automaticly

    # foreign keys
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    # columns

    end_date = models.DateField()
    type = models.CharField(max_length=1, choices=TYPES)
    description = models.CharField(max_length=128)
    objects = GoalsManager()

class Files(models.Model):

    # pk generated automaticly

    # foreign keys
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    # TODO: sposob zapisywania?
    file_path = models.CharField(max_length=30)
    description = models.CharField(max_length=64, blank=True)
    objects = FilesManager()

class Prediction(models.Model):

    # pk generated automaticly

    # foreign keys
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    start_date = models.DateField(default=timezone.now)
    pred_time = models.TimeField()
    actual_time = models.TimeField()
    objects = PredictionManager()


class Events(models.Model):

    TYPES = [
    ("ONCE", "Once"),
    ("DAILY", "Daily"),
    ("WEEKLY", "Weekly"),
    ("MONTHLY", "Monthly"),
    ("YEARLY", "Yearly"),
    ("EVEN", "Even"),
    ("ODD", "Odd")
    ]
    # pk generated automaticly

    # foreign keys
    client_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    period_type = models.CharField(choices=TYPES, max_length=7)
    objects = EventsManager()



class Description(models.Model):


    event_id = models.OneToOneField(
    Events,
    on_delete = models.CASCADE,
    primary_key=True,
    )
    course = models.BooleanField()
    description = models.CharField(max_length=128)
    objects = DescriptionManager()


class Marks(models.Model):
    # pk generated automaticly
    TYPES = [
    ("PLUS", "+"),
    ("MINUS", "-"),
    ("PKT", "pkt"),
    ("MARK", "mark"),
    ]
    course_id = models.OneToOneField(
    Course,
    on_delete = models.CASCADE,
    )
    mark = models.IntegerField()
    weight = models.IntegerField()
    mark_type = models.CharField(choices=TYPES, max_length=7)
    objects = MarksManager()
