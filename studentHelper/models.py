from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.title

class Teacher(models.Model):

    # pk generated automaticly

    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    webpage = models.CharField(max_length=60)

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


class Events(models.Model):

    TYPES = [
    ("once", "Once"),
    ("daily", "Daily"),
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("yearly", "Yearly"),
    ("even", "Even"),
    ("odd", "Odd")
    ]
    # pk generated automaticly

    # foreign keys
    client_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    period_type = models.CharField(choices=TYPES, max_length=7)


class Description(models.Model):


    event_id = models.OneToOneField(
    Events,
    on_delete = models.CASCADE,
    primary_key=True,
    )
    course = models.BooleanField()
    description = models.CharField(max_length=128)
