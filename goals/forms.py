from studentHelper.models import Goals, Course
from bootstrap_datepicker_plus import DateTimePickerInput
from django.forms import ModelForm, Form, ChoiceField
from django.core.exceptions import ValidationError
from django.utils import timezone


class GoalsForm(ModelForm):
    class Meta:
        model = Goals
        fields = ['end_date', 'type', 'value', 'description']
        widgets = {
            'end_date': DateTimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['end_date'].label = 'Termin, do którego cel ma zostać osiągnięty'
        self.fields['type'].label = 'Typ'
        self.fields['value'].label = 'Wartość'
        self.fields['description'].label = 'Opis'
        for key in self.fields:
            self.fields[key].error_messages['required'] = 'To pole jest wymagane.'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('value') < 0:
            raise ValidationError('Wartość celu do osiągnięcia nie może być ujemna!')
        if cleaned_data.get('end_date').date() < timezone.now().date():
            raise ValidationError('Osiągnięcie celu zanim się go wyznaczyło? Czy to ty, Heistotron?')


class CourseForm(Form):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client')
        super().__init__(*args, **kwargs)
        courses = Course.objects.get_records_by_client_id(self.client)
        options = [(c.course_name+' '+c.type, c.course_name+' '+c.type) for c in courses]
        self.fields['course'] = ChoiceField(choices=options)
        self.fields['course'].label = 'Kurs'
        self.fields['course'].error_messages['required'] = 'To pole jest wymagane.'
