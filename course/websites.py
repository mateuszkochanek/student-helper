import requests
from bs4 import BeautifulSoup
import difflib
import time
from django.conf import settings
from django.core.mail import send_mail
from studentHelper.models import *
from studentHelper.managers import *
from webpush import send_user_notification
from urllib.parse import urljoin
import threading


def get_diff(out_text):
    msg = ''
    for i in range(0, len(out_text)):
        if (out_text[i] == '+' or out_text[i] == '-') and out_text[i + 1] == '\n':
            i += 2
        elif out_text[i] == '+' or out_text[i] == '-':
            while i < len(out_text) and out_text[i] != '\n':
                msg += out_text[i]
                i += 1
            msg += '\n'

    return msg


class WebsiteMonitoring(threading.Thread):

    def __init__(self, url, request, course_id, teacher_id, course):

        threading.Thread.__init__(self)

        self.request = request
        self.url = url
        self.course_id = course_id
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.prev_version = Teacher.objects.get_record_by_id(teacher_id).html
        self.first_run = True
        self.old_page = ""
        self.new_page = ""

        self.pdf = []
        self.teacher_id = teacher_id
        self.course = course

    def check_changes(self):
        response = requests.get(self.url, headers=self.headers)
        r = response.text
        self.course.teacher_id.html = r
        self.course.teacher_id.save()
        soup = BeautifulSoup(r, "html.parser")

        for link in soup.select("a[href$='.pdf']"):
            url = urljoin(self.url, link['href'])
            filename = link['href'].split('/')[-1]
            if Files.objects.get_record_by_file_path(self.course, filename, self.teacher_id) is None:
                self.send_push_pdf(url)
                course = Course.objects.get_record_by_id(self.course_id)
                Files.objects.add_record(course, filename, str(self.teacher_id))

        for script in soup(["script", "style"]):
            script.extract()
        soup = soup.get_text()

        self.prev_version = BeautifulSoup(self.prev_version, "html.parser")
        for script in self.prev_version(["script", "style"]):
            script.extract()
        self.prev_version = self.prev_version.get_text()

        if self.prev_version != soup:
            self.old_page = self.prev_version.splitlines()
            self.new_page = soup.splitlines()
            d = difflib.Differ()
            diff = d.compare(self.old_page, self.new_page)
            out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])
            msg = get_diff(out_text)
            self.send_email(msg)
            self.send_push()

    def send_email(self, msg):
        subject = 'Zmiany na stronie prowadzącego'
        message = f'Cześć {self.request.user.username},\n Na stronie ' + self.url + 'zostały wykryte następujące ' \
                                                                                    'zmiany: \n '
        message += msg
        print(message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email, ]
        send_mail(subject, message, email_from, recipient_list)

    def add_list(self):
        Files.objects.delete_by_course_id_and_description(self.course, str(self.teacher_id))
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.select("a[href$='.pdf']"):
            filename = link['href'].split('/')[-1]
            course = Course.objects.get_record_by_id(self.course_id)
            Files.objects.add_record(course, filename, str(self.teacher_id))

    def send_push(self):
        payload = {"head": "Zmiany na stronie", "body": "Kliknij tutaj, żeby zobaczyć aktualną wersję "
                                                        "strony. Szczegóły zmian zostały wysłane na Twój adres email",
                                                        "icon": "https://i.imgur.com/dRDxiCQ.png", "url": self.url}
        send_user_notification(user=self.request.user, payload=payload, ttl=1000)

    def send_push_pdf(self, url):
        payload = {"head": "Nowa lista", "body": "Kliknij tutaj, żeby obejrzeć nowo dodaną listę",
                                                        "icon": "https://i.imgur.com/dRDxiCQ.png", "url": url}
        send_user_notification(user=self.request.user, payload=payload, ttl=1000)
