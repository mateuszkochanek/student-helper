from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Events, Description
from django.contrib.admin import widgets


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['start_date', 'end_date', 'period_type']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].label = "Początek wydarzenia"
        # self.fields["start_date"].widget = widgets.AdminSplitDateTime()
            # self.fields["start_date"].widget = self.SelectDateWidget()
        self.fields["end_date"].label = "Koniec wydarzenia"
        # self.fields["end_date"].widget = widgets.AdminSplitDateTime()
        self.fields["period_type"].label = "Okres trwania"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def form_valid(self, form):
        print("WIIIIIIITAM", form.instance.client_id)
        form.instance.client_id = self.request.user
        return super().form_valid(form)

class DescriptionForm(forms.ModelForm):

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
