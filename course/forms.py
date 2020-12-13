from studentHelper.models import Marks, Teacher
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import Form, CheckboxSelectMultiple, MultipleChoiceField, FloatField, ChoiceField
from studentHelper.models import Components, Thresholds, CourseGroup, Modyfication, Course


class MarkForm(ModelForm):

    class Meta:
        model = Marks
        fields = ['mark', 'weight', 'mark_type', 'mark_form']

    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop('course_id')
        super().__init__(*args, **kwargs)
        self.fields["mark"].label = "Ocena"
        self.fields["weight"].label = "Waga oceny"
        self.fields["mark_type"].label = "Typ oceny"
        self.fields["mark_form"].label = "Otrzymana za"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def clean(self):
        cleaned_data = super().clean()
        components = Components.objects.get_records_by_course_id(self.course_id).values("form", "type")

        check = {}
        for el in components:
            check.update({el['form']: el['type']})

        mark = cleaned_data.get("mark")
        weight = cleaned_data.get("weight")
        mark_form = cleaned_data.get("mark_form")
        mark_type = cleaned_data.get("mark_type")
        if mark and weight and mark_form and mark_type:
            if mark_type == "PLUS" or mark_type == "MINUS":
                mark_type = "PKT"
            if mark < 1:
                raise ValidationError(
                    "Chyba ciężko otrzymać taką ocenę :o"
                )
            elif weight < 0:
                raise ValidationError(
                    "Hmmm, ujemna waga?"
                )


class TeacherForm(ModelForm):

    class Meta:
        model = Teacher
        fields = ['webpage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["webpage"].label = "Strona prowadzącego"
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def clean(self):
        cleaned_data = super().clean()
        webpage = cleaned_data.get("webpage")
        # TODO check if site was input correctly

            elif mark_form not in check:
                raise ValidationError(
                    "Nieprawidłowy typ oceny!"
                )

            elif check[mark_form] != mark_type:
                raise ValidationError(
                    "Forma otrzymania oceny nie zgadza się z jej typem!"
                )


class RulesForm(Form):

    def __init__(self, *args, **kwargs):
        self.course_id = Course.objects.get_record_by_id(kwargs.pop('course_id'))
        super().__init__(*args, **kwargs)
        FORMS = (
            ('aktywność', 'aktywność'),
            ('egzamin', 'egzamin'),
            ('kartkówka', 'kartkówka'),
            ('kolokwium', 'kolokwium'),
            ('lista zadań', 'lista zadań')
        )
        TYPES = (
            ('punkty', 'punkty'),
            ('ocena', 'ocena'),
            ('procenty', 'procenty'),
        )
        self.fields['formy'] = MultipleChoiceField(widget=CheckboxSelectMultiple, choices=FORMS)
        self.fields['formy'].label = '1. Wybierz formy uzyskania ocen cząstkowych na kursie:'
        i = 2
        for form in FORMS:
            t_name = '{}_t'.format(form[0])
            self.fields[t_name] = ChoiceField(choices=TYPES, required=False)
            self.fields[t_name].label = '{0:d}. Zaznacz rodzaj oceniania formy: {1}'.format(i, form[0])
            i += 1

        self.fields['thresh_type'] = ChoiceField(choices=TYPES)
        self.fields['thresh_type'].label = '{0:d}. Wybierz typ w jakim jest skala, według której wystawiana jest' \
                                           ' ocena końcowa:'.format(i)
        i += 1
        mark = 2
        half = 0
        j = 0
        while mark+half < 6:
            name_p = 'p_{0:d}_{1:d}'.format(mark, int(half*10))
            name_k = 'k_{0:d}_{1:d}'.format(mark, int(half*10))
            if mark != 2 or half != 0:
                self.fields[name_p] = FloatField(min_value=0, required=True)
                self.fields[name_p].label = 'Początek zakresu dla oceny {0:.1f}'.format(mark+half)
            if mark != 5 or half != 0.5:
                self.fields[name_k] = FloatField(required=True)
                self.fields[name_k].label = 'Koniec zakresu dla oceny {0:.1f}'.format(mark + half)
            if j % 2 == 0:
                half += 0.5
            else:
                mark += 1
                half = 0
            j += 1

    def save(self):
        enum_form = {
            'aktywność': 'ACTIV',
            'egzamin': 'EXAM',
            'kartkówka': 'QUIZ',
            'kolokwium': 'TEST',
            'lista zadań': 'LIST'
        }
        enum_type = {
            'punkty': 'POINT',
            'procenty': 'PERC',
            'ocena': 'MARK'
        }
        for form in self.cleaned_data['formy']:
            Components.objects.add_record(self.course_id, enum_form[form],
                                          enum_type[self.cleaned_data['{}_t'.format(form)]])
        Thresholds.objects.add_record(self.course_id, self.cleaned_data['k_2_0'],
                                      self.cleaned_data['p_2_5'], self.cleaned_data['k_2_5'],
                                      self.cleaned_data['p_3_0'], self.cleaned_data['k_3_0'],
                                      self.cleaned_data['p_3_5'], self.cleaned_data['k_3_5'],
                                      self.cleaned_data['p_4_0'], self.cleaned_data['k_4_0'],
                                      self.cleaned_data['p_4_5'], self.cleaned_data['k_4_5'],
                                      self.cleaned_data['p_5_0'], self.cleaned_data['k_5_0'],
                                      self.cleaned_data['p_5_5'], enum_type[self.cleaned_data['thresh_type']])
