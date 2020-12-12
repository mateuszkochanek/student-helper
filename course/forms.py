from studentHelper.models import Marks
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class MarkForm(ModelForm):

    class Meta:
        model = Marks
        fields = ['mark', 'weight', 'mark_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mark"].label = "Ocena"
        self.fields["weight"].label = "Waga oceny"
        self.fields["mark_type"].label = "Typ oceny"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def clean(self):
        cleaned_data = super().clean()
        mark = cleaned_data.get("mark")
        weight = cleaned_data.get("weight")

        if mark and weight:
            if mark < 0:
                raise ValidationError(
                    "Jaki prowadzący daje ujemne oceny?"
                )
            elif weight < 0:
                raise ValidationError(
                    "Hmmm, ujemna waga?"
                )
