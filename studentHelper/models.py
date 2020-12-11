from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse


from studentHelper.managers import *



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
    ("W", "wykład"),
    ("C", "ćwiczenia"),
    ("L", "laboratoria"),
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
    final = models.FloatField(blank=True, default=0)
    objects = CourseManager()



class Components(models.Model):

    FORMS = [
    ("ACTIV", "aktywność"),
    ("EXAM", "egzamin"),
    ("QUIZ", "kartkówka"),
    ("TEST", "kolokwium"),
    ("LIST", "lista zadań"),
    ]

    TYPES = [
    ("POINT", "punkty"),
    ("MARK", "ocena"),
    ("PERC", "procent"),
    ]

    course_id = models.OneToOneField(
    Course,
    on_delete = models.CASCADE,
    primary_key=True,
    )


    form = models.CharField(max_length=5, choices=FORMS)
    weight = models.FloatField()
    type = models.CharField(max_length=5, choices=TYPES)
    objects = ComponentsManager()

class Thresholds(models.Model):

    TYPES = [
    ("POINT", "punkty"),
    ("MARK", "ocena"),
    ("PERC", "procent"),
    ]

    course_id = models.OneToOneField(
    Course,
    on_delete = models.CASCADE,
    primary_key=True,
    )


    p_2_0 = models.FloatField()
    k_2_0 = models.FloatField()
    p_2_5 = models.FloatField()
    k_2_5 = models.FloatField()
    p_3_0 = models.FloatField()
    k_3_0 = models.FloatField()
    p_3_5 = models.FloatField()
    k_3_5 = models.FloatField()
    p_4_0 = models.FloatField()
    k_4_0 = models.FloatField()
    p_4_5 = models.FloatField()
    k_4_5 = models.FloatField()
    p_5_0 = models.FloatField()
    k_5_0 = models.FloatField()
    p_5_5 = models.FloatField()
    k_5_5 = models.FloatField()
    type = models.CharField(max_length=5, choices=TYPES)
    objects = ComponentsManager()


class Modyfication(models.Model):

    TYPES = [
    ("POINT", "punkty"),
    ("MARK", "ocena"),
    ("PERC", "procent"),
    ]

    MOD = [
    ("MINUS", "-"),
    ("PLUS", "+"),
    ]

    course_id = models.OneToOneField(
    Course,
    on_delete = models.CASCADE,
    primary_key=True,
    )

    mod = models.CharField(max_length=5, choices=MOD)
    val = models.FloatField()
    type = models.CharField(max_length=5, choices=TYPES)
    objects = ModyficationManager()


class CourseGroup(models.Model):

    course_id = models.OneToOneField(
    Course,
    on_delete = models.CASCADE,
    primary_key=True,
    )

    weight = models.FloatField()
    minimum = models.BooleanField(default=False)
    objects = CourseGroupManager()


class Goals(models.Model):

    TYPES = [
    ("A", "aktywność"),
    ("M", "ocena"),
    ("O", "inne"),
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
    ("ONCE", "Pojedyncze wydarzenie"),
    ("DAILY", "Codziennie"),
    # ("WEEKLY", "Weekly"),
    # ("MONTHLY", "Monthly"),
    # ("YEARLY", "Yearly"),
    # ("EVEN", "Even"),
    # ("ODD", "Odd")
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
    course = models.BooleanField(default=False)
    description = models.CharField(max_length=128)
    objects = DescriptionManager()


class Marks(models.Model):
    # pk generated automaticly
    TYPES = [
    ("PLUS", "+"),
    ("MINUS", "-"),
    ("PKT", "pkt"),
    ("MARK", "ocena"),
    ]
    course_id = models.OneToOneField(
    Course,
    on_delete = models.CASCADE,
    )
    mark = models.IntegerField()
    weight = models.IntegerField()
    mark_type = models.CharField(choices=TYPES, max_length=7)
    objects = MarksManager()
