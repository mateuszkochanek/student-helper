from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Events, Description
from bootstrap_datepicker_plus import DateTimePickerInput
from django.forms import ModelForm
from django.core.exceptions import ValidationError



# pip install django-bootstrap-datepicker-plus
# pip install django-bootstrap4


class EventForm(ModelForm):

    class Meta:
        model = Events
        fields = ['start_date', 'end_date', 'period_type']
        widgets = {
            'start_date': DateTimePickerInput(),
            'end_date': DateTimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].label = "Początek wydarzenia"
        self.fields["end_date"].label = "Koniec wydarzenia"
        self.fields["period_type"].label = "Okres trwania"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError(
                    "Podróż w czasie jest niemożliwa :)"
                )


class DescriptionForm(ModelForm):

    class Meta:
        model = Description
        fields = ['course', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].label = "Czy jest to kurs?"
        self.fields["course"].help_text = "Wymagane. True lub False"
        self.fields["description"].label = "Opis"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."
