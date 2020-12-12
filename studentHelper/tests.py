from django.test import TestCase
from .models import Course, Teacher
from avgGrade.avg import get_avg
from django.contrib.auth.models import User


# Create your tests here.
class AvgTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'mail@gmail.com', 'psswd')
        user2 = User.objects.create_user('test2', 'test@mail.com', 'psswd')
        teacher = Teacher.objects.create(name='testowy', surname='wykladowca', title='dr hab.', webpage='abc.pl')
        Course.objects.create(client_id=user, teacher_id=teacher, ECTS=1, name="test1", type="W", final=3)
        Course.objects.create(client_id=user, teacher_id=teacher, ECTS=2, name="test2", type="W", final=4.5)
        Course.objects.create(client_id=user, teacher_id=teacher, ECTS=3, name="test3", type="W", final=5)
        Course.objects.create(client_id=user, teacher_id=teacher, ECTS=4, name="test4", type="W", final=3.5)
        Course.objects.create(client_id=user2, teacher_id=teacher, ECTS=3, name="test5", type="W", final=5)
        Course.objects.create(client_id=user2, teacher_id=teacher, ECTS=4, name="test6", type="W", final=0)

    def testAvg(self):
        self.assertEqual(get_avg(1), 4.1)
        self.assertEqual(get_avg(2), -1)