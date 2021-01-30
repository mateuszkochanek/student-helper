import requests
from bs4 import BeautifulSoup
import difflib
import time
from django.conf import settings
from django.core.mail import send_mail


def get_diff(out_text):
    msg = ''
    for i in range(0, len(out_text)):
        if out_text[i] == '+' or out_text[i] == '-':
            while i < len(out_text) and out_text[i] != '\n':
                msg += out_text[i]
                i += 1
            msg += '\n'

    return msg


class WebsiteMonitoring:

    def __init__(self, url, request):
        self.request = request
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.prev_version = ""
        self.first_run = True
        self.old_page = ""
        self.new_page = ""

    def monitoring(self):
        while True:
            self.check_changes()

    def check_changes(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        soup = soup.get_text()
        if self.prev_version != soup:
            if self.first_run:
                self.prev_version = soup
                self.first_run = False
            else:
                self.old_page = self.prev_version.splitlines()
                self.new_page = soup.splitlines()
                d = difflib.Differ()
                diff = d.compare(self.old_page, self.new_page)
                out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])
                msg = get_diff(out_text)
                self.send_email(msg)
                self.old_page = self.new_page
                self.prev_version = soup
        time.sleep(100)

    def send_email(self, msg):
        subject = 'Zmiany na stronie prowadzącego'
        message = f'Cześć {self.request.user.username},\n Na stronie ' + self.url + 'zostały wykryte następujące ' \
                                                                                    'zmiany: \n '
        message += msg
        print(message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email, ]
        send_mail(subject, message, email_from, recipient_list)
