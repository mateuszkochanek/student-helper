from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from studentHelper.models import Events, Description, Course, Teacher, CourseEvents, Prediction
from bootstrap_datepicker_plus import DateTimePickerInput
from django.forms import Form, ModelForm, TimeField, DateInput, FloatField, ChoiceField, HiddenInput
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.forms.widgets import HiddenInput
from django.contrib.admin import widgets
from datetime import timedelta
import validators

# pip install django-bootstrap-datepicker-plus
# pip install django-bootstrap4


class EventForm(ModelForm):

    class Meta:
        model = Events
        fields = ['start_date', 'end_date', 'period_type', 'whole_day']
        widgets = {
            'start_date': DateTimePickerInput(),
            'end_date': DateTimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].label = "Początek wydarzenia"
        self.fields["end_date"].label = "Koniec wydarzenia"
        self.fields["period_type"].label = "Okres trwania"
        self.fields["whole_day"].label = "Cały dzień"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        period = cleaned_data.get("period_type")

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError(
                    "Podróż w czasie jest niemożliwa :)"
                )
            elif period == "ONCE" and start_date.date() != end_date.date():
                raise ValidationError(
                    "Pojedyncze wydarzenie = Wydarzenie w jednym dniu. \n \
                    Co tutaj jest niejasne? :D"
                )

            elif start_date < timezone.now().replace(hour=0, minute=0, second=0):
                raise ValidationError(
                    "Po co dodawać wydarzenia, które już się nie spełnią? :o"
                )
            elif period == "DAILY" and start_date.date() == end_date.date():
                raise ValidationError(
                    "Opcja codziennie wymaga co najmniej dwóch dni -_- "
                )
            elif period == "WEEKLY" and end_date.date() - start_date.date() < timedelta(days=14):
                raise ValidationError(
                    "Opcja tygodniowo wymaga co najmniej dwóch tygodni -_- "
                )
            elif period == "MONTHLY" and end_date.date() - start_date.date() < timedelta(days=58):
                raise ValidationError(
                    "Opcja miesięcznie wymaga co najmniej dwóch miesięcy -_- "
                )
            elif period == "YEARLY" and end_date.date() - start_date.date() < timedelta(days=365):
                raise ValidationError(
                    "Opcja rocznie wymaga co najmniej dwóch lat -_- "
                )
class CourseEventForm(ModelForm):

    class Meta:
        model = CourseEvents
        fields = ['start_date', 'end_date', 'period_type', 'whole_day', 'description']
        widgets = {
            'start_date': DateTimePickerInput(),
            'end_date': DateTimePickerInput(),
        }

    def __init__(self, *args, **kwargs):

        show_desc = False
        try:
            self.desc = kwargs.pop('desc')
        except:
            show_desc = True

        super().__init__(*args, **kwargs)

        self.fields["start_date"].label = "Początek wydarzenia"
        self.fields["end_date"].label = "Koniec wydarzenia"
        self.fields["period_type"].label = "Okres trwania"
        self.fields["whole_day"].label = "Cały dzień"
        self.fields["description"].label = "Opis"
        if not show_desc:
            self.fields["description"].initial = self.desc

        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        period = cleaned_data.get("period_type")


        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError(
                    "Podróż w czasie jest niemożliwa :)"
                )
            elif period == "ONCE" and start_date.date() != end_date.date():
                raise ValidationError(
                    "Pojedyncze wydarzenie = Wydarzenie w jednym dniu. \n \
                    Co tutaj jest niejasne? :D"
                )

            elif start_date < timezone.now().replace(hour=0, minute=0, second=0):
                raise ValidationError(
                    "Po co dodawać wydarzenia, które już się nie spełnią? :o"
                )
            elif period == "DAILY" and start_date.date() == end_date.date():
                raise ValidationError(
                    "Opcja codziennie wymaga co najmniej dwóch dni -_- "
                )
            elif period == "WEEKLY" and end_date.date() - start_date.date() < timedelta(days=14):
                raise ValidationError(
                    "Opcja tygodniowo wymaga co najmniej dwóch tygodni -_- "
                )
            elif period == "MONTHLY" and end_date.date() - start_date.date() < timedelta(days=58):
                raise ValidationError(
                    "Opcja miesięcznie wymaga co najmniej dwóch miesięcy -_- "
                )
            elif period == "YEARLY" and end_date.date() - start_date.date() < timedelta(days=365):
                raise ValidationError(
                    "Opcja rocznie wymaga co najmniej dwóch lat -_- "
                )

class DescriptionForm(ModelForm):

    class Meta:
        model = Description
        fields = ['description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].label = "Opis"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

class DescourseForm(ModelForm):

    class Meta:
        model = Description
        fields = ['course', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].widget = HiddenInput()
        self.fields["course"].initial = True
        self.fields["description"].label = "Opis"
        self.fields["description"].help_text = "To będzie wyświetlane w kalendarzu"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

class CourseForm(ModelForm):

    class Meta:
        model = Course
        fields = ['course_name', 'ECTS', 'type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course_name"].label = "Nazwa kursu"
        self.fields["course_name"].help_text = "Poprawna nazwa kursu"
        self.fields["ECTS"].label = "ECTS"
        self.fields["ECTS"].initial = 0
        self.fields["type"].label = "Typ zajęć"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def clean(self):
        cleaned_data = super().clean()
        ects = cleaned_data.get("ECTS")

        if ects:
            if ects < 0:
                raise ValidationError(
                    "Nie możesz być aż tak słabym uczniem ;)"
                )


class TeacherForm(ModelForm):

    class Meta:
        model = Teacher
        fields = ['name', 'surname', 'title', 'webpage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Imię prowadzącego"
        self.fields["surname"].label = "Nazwisko prowadzącego"
        self.fields["title"].label = "Tytuł prowadzącego"
        self.fields["webpage"].label = "Strona internetowa prowadzącego"
        self.fields["webpage"].initial = "brak"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def clean(self):
        cleaned_data = super().clean()
        webpage = cleaned_data.get("webpage")
        if webpage is not None and webpage is not "":
            valid=validators.url(webpage)
            if not valid:
                raise ValidationError(
                    "Błędny adres strony"
                )


class PredTimeForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        TYPES = [
        ("EXAM", "egzamin"),
        ("QUIZ", "kartkówka"),
        ("TEST", "kolokwium"),
        ("LIST", "lista zadań"),
        ]

        self.fields["choices"] = ChoiceField(choices=TYPES)
        self.fields["choices"].label = "Opis"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def save(self):
        return self.cleaned_data['choices']


    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['choices'] = cleaned_data['choices']


class PredictionForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["actual_time"] = FloatField()
        self.fields["actual_time"].label = "Czas wykonania (w minutach)"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def save(self, prediction):
        prediction.actual_time = self.cleaned_data['actual_time'] * 60
        prediction.save()

    def clean(self):
        cleaned_data = super().clean()
        time = cleaned_data['actual_time']
        self.cleaned_data['actual_time'] = cleaned_data['actual_time']
        print(self.cleaned_data['actual_time'])
        if time < 0:
            raise ValidationError('Czas nie może być ujemny!')
