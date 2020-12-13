from studentHelper.models import Marks, Teacher
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import Form, CheckboxSelectMultiple, MultipleChoiceField, FloatField, ChoiceField, IntegerField
from studentHelper.models import Components, Thresholds, CourseGroup, Modyfication, Course


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
        i = 1
        self.fields['ects'] = IntegerField(min_value=0, max_value=30)
        self.fields['ects'].label = '{0:d} Wpisz ile punktów ECTS ma kurs:'.format(i)
        i += 1
        self.fields['formy'] = MultipleChoiceField(widget=CheckboxSelectMultiple, choices=FORMS)
        self.fields['formy'].label = '{0:d}. Wybierz formy uzyskania ocen cząstkowych na kursie:'.format(i)
        i += 1
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

        YN = (
            ('Tak', 'Tak'),
            ('Nie', 'Nie')
        )
        self.fields['mod_plus'] = ChoiceField(choices=YN)
        self.fields['mod_plus'].label = '{0:d}. Czy możliwe jest podwyższenie oceny?'.format(i)
        i += 1
        self.fields['mod_plus_t'] = ChoiceField(choices=TYPES, required=False)
        self.fields['mod_plus_t'].label = 'Wybierz w jakim typie jest modyfikacja oceny:'
        self.fields['mod_plus_w'] = FloatField(min_value=0, required=False)
        self.fields['mod_plus_w'].label = 'Wpisz o ile ocena może zostać podwyższona:'

        self.fields['mod_minus'] = ChoiceField(choices=YN)
        self.fields['mod_minus'].label = '{0:d}. Czy możliwe jest obniżenie oceny?'.format(i)
        i += 1
        self.fields['mod_minus_t'] = ChoiceField(choices=TYPES, required=False)
        self.fields['mod_minus_t'].label = 'Wybierz w jakim typie jest modyfikacja oceny:'
        self.fields['mod_minus_w'] = FloatField(min_value=0, required=False)
        self.fields['mod_minus_w'].label = 'Wpisz o ile ocena może zostać obniżona:'

        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."
            if 'invalid' in self.fields[key].error_messages:
                self.fields[key].error_messages['invalid'] = 'To nie jest poprawna wartość'
            if 'min_value' in self.fields[key].error_messages:
                self.fields[key].error_messages['min_value'] = 'To nie jest poprawna wartość'
            if 'max_value' in self.fields[key].error_messages:
                self.fields[key].error_messages['max_value'] = 'To nie jest poprawna wartość'

    def save(self):
        enum_form = {
            'aktywność': 'ACTIV',
            'egzamin': 'EXAM',
            'kartkówka': 'QUIZ',
            'kolokwium': 'TEST',
            'lista zadań': 'LIST'
        }
        enum_type = {
            'punkty': 'PKT',
            'procenty': 'PERC',
            'ocena': 'MARK'
        }
        if not Components.objects.get_records_by_course_id(self.course_id):

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

            if self.cleaned_data['mod_plus'] == 'Tak':
                Modyfication.objects.add_record(self.course_id, 'PLUS', self.cleaned_data['mod_plus_w'],
                                                enum_type[self.cleaned_data['mod_plus_t']])
            if self.cleaned_data['mod_minus'] == 'Tak':
                Modyfication.objects.add_record(self.course_id, 'MINUS', self.cleaned_data['mod_minus_w'],
                                                enum_type[self.cleaned_data['mod_minus_t']])
            self.course_id.ECTS = self.cleaned_data['ects']
            self.course_id.save()

    def clean(self):
        thresholds = [self.cleaned_data['k_2_0']]
        mark = 3
        half = 0
        j = 0
        while mark + half < 6:
            name_p = 'p_{0:d}_{1:d}'.format(mark, int(half * 10))
            thresholds.append(self.cleaned_data[name_p])
            if mark != 5 or half != 0.5:
                name_k = 'k_{0:d}_{1:d}'.format(mark, int(half * 10))
                thresholds.append(self.cleaned_data[name_k])
            if j % 2 == 0:
                half += 0.5
            else:
                mark += 1
                half = 0
            j += 1
        prev = thresholds[0]
        for i in range(1, len(thresholds)):
            if thresholds[i] <= prev:
                raise ValidationError('Wyższa ocena = wyższy próg, nie?')
            prev = thresholds[i]

        if self.cleaned_data['mod_minus'] == 'Tak' and self.cleaned_data['mod_minus_w'] is None:
            raise ValidationError('Jeżeli jest dostępna modyfikacja oceny, to na pewno wiadomo o ile')

        if self.cleaned_data['mod_plus'] == 'Tak' and self.cleaned_data['mod_plus_w'] is None:
            raise ValidationError('Jeżeli jest dostępna modyfikacja oceny, to na pewno wiadomo o ile')
