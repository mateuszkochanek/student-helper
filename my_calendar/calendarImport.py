from icalendar import Calendar, Event
import itertools
import easygui
import threading
from studentHelper.models import Teacher, Course, Events, Description, Marks, Goals, Files, Prediction
from django.contrib.auth.models import User

def get_teacher_data(teacher):
    t = teacher.split()
    name = t[len(t) - 2]
    surname = t[len(t) - 1]
    title = t[0:len(t) - 2]
    title2 = ''
    for i in title:
        title2 += i
        title2 += ' '
    return name, surname, title2


class CalendarImport(threading.Thread):

    def __init__(self, user):

        threading.Thread.__init__(self)

        self.AllTeachers = []
        self.AllCourses = []
        self.AllEvents = []
        self.user = user

        file = easygui.fileopenbox()
        try:
            if file is not None:
                f = open(file, 'rb')
                gcal = Calendar.from_ical(f.read())

                self.read_calendar(gcal)
                self.clear_tables()
                self.add_to_dbase()
        except ValueError:
            print("Cos nie tak z plikiem")

    def clear_tables(self):
        Events.objects.filter(client_id=self.user.id, description__course=True).delete()
        Course.objects.get_records_by_client_id(self.user.id).delete()

    def read_calendar(self, calendar):
        course = {'dtstart': '', 'dtend': '', 'description': '', 'location': '', 'summary': ''}

        for component in calendar.walk():
            if component.name == "VEVENT":
                summary = component.get('summary')
                description = component.get('description')
                if description not in self.AllTeachers:
                    self.AllTeachers.append(description)
                location = component.get('location')
                startdt = component.get('dtstart').dt
                enddt = component.get('dtend').dt

                courseData = {'description': description, 'location': location,
                              'summary': summary, 'dtstart': startdt, 'dtend': enddt}
                self.AllEvents.append(courseData)

        list_dicts = list()
        for name, group in itertools.groupby(sorted(self.AllEvents, key=lambda d: d['summary']), key=lambda d: d['summary']):
            list_dicts.append(next(group))

        sortedList = sorted(list_dicts, key=lambda k: k['summary'][2:])

        sameCourse = []
        i = 0
        for item in sortedList:
            if i == 0:
                earlier = item
                i += 1
                sameCourse.append(item)
            else:
                if item['summary'][2:] == earlier['summary'][2:]:
                    sameCourse.append(item)
                else:
                    self.AllCourses.append(sameCourse)
                    sameCourse = [item]
                    earlier = item


    def add_to_dbase(self):
        for teacher in self.AllTeachers:
            name, surname, title = get_teacher_data(teacher)
            Teacher.objects.add_record(name, surname, title, '')

        for course2 in self.AllCourses:
            for course in course2:
                name, surname, title = get_teacher_data(course['description'])
                teacher = Teacher.objects.get_record_by_name_surname_title(name, surname, title)
                if self.user.is_authenticated:
                    Course.objects.add_record(self.user, teacher, 0, course['summary'][2:], course['summary'][0])

        for events in self.AllEvents:
            if self.user.is_authenticated:
                e = Events.objects.add_record(self.user, events['dtstart'], events['dtend'], 'ONCE')
                #Todo gdzie nazwa kursu?!
                Description.objects.add_record(e, True, events['summary'][2:])
