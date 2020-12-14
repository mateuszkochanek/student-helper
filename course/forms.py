from studentHelper.models import Marks, Teacher
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import Form, CheckboxSelectMultiple, MultipleChoiceField, FloatField, ChoiceField, IntegerField
from studentHelper.models import Components, Thresholds, CourseGroup, Modyfication, Course
import validators



class WebPageForm(ModelForm):

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

        if webpage is not None:
            valid=validators.url(webpage)
            if not valid:
                raise ValidationError(
                    "Błędny adres strony"
                )


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


class ThresholdsForm(ModelForm):

    class Meta:
        model = Thresholds
        fields = ['type', 'p_3_0', 'p_3_5',  'p_4_0', 'p_4_5',  'p_5_0', 'p_5_5']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['type'].label = "Wybierz typ w jakim jest skala, według której wystawiana jest \
                                          ocena końcowa "
        mark = 3.0
        self.marks = ['p_3_0', 'p_3_5', 'p_4_0', 'p_4_5', 'p_5_0', 'p_5_5']

        for key in self.marks:
            self.fields[key].label = "Początek zakresu dla oceny " + str(mark)
            mark += 0.5
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."

    def clean(self):
        cleaned_data = super().clean()
        prev = cleaned_data.get('p_5_5')
        self.marks = self.marks[:-1]

        for key in self.marks[::-1]:
            mark = cleaned_data.get(key)
            if mark < 0:
                raise ValidationError('Czy za ujemne oceny trzeba płacić?')
            if mark > prev:
                raise ValidationError('Wyższa ocena = wyższy próg, nie?')
            prev = mark


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
            if self.cleaned_data['mod_plus'] == 'Tak':
                Modyfication.objects.add_record(self.course_id, 'PLUS', self.cleaned_data['mod_plus_w'],
                                                enum_type[self.cleaned_data['mod_plus_t']])
            if self.cleaned_data['mod_minus'] == 'Tak':
                Modyfication.objects.add_record(self.course_id, 'MINUS', self.cleaned_data['mod_minus_w'],
                                                enum_type[self.cleaned_data['mod_minus_t']])
            self.course_id.ECTS = self.cleaned_data['ects']
            self.course_id.save()

    def clean(self):

        if self.cleaned_data['mod_minus'] == 'Tak' and self.cleaned_data['mod_minus_w'] is None:
            raise ValidationError('Jeżeli jest dostępna modyfikacja oceny, to na pewno wiadomo o ile')

        if self.cleaned_data['mod_plus'] == 'Tak' and self.cleaned_data['mod_plus_w'] is None:
            raise ValidationError('Jeżeli jest dostępna modyfikacja oceny, to na pewno wiadomo o ile')

    def fill_edit(self):
        enum_form = {
            'ACTIV': 'aktywność',
            'EXAM': 'egzamin',
            'QUIZ': 'kartkówka',
            'TEST': 'kolokwium',
            'LIST': 'lista zadań'
        }
        enum_type = {
            'PKT': 'punkty',
            'PERC': 'procenty',
            'MARK': 'ocena'
        }
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
        YN = (
            ('Tak', 'Tak'),
            ('Nie', 'Nie')
        )
        comp = Components.objects.get_records_by_course_id(self.course_id)
        ects = self.course_id.ECTS
        mod = Modyfication.objects.get_records_by_course_id(self.course_id)
        print(mod)
        i = 1
        self.fields['ects'] = IntegerField(min_value=0, max_value=30, initial=ects)
        self.fields['ects'].label = '{0:d} Wpisz ile punktów ECTS ma kurs:'.format(i)
        i += 1
        init_comp = []
        for c in comp:
            init_comp.append(enum_form[c.form])
        self.fields['formy'] = MultipleChoiceField(widget=CheckboxSelectMultiple, choices=FORMS, initial=init_comp)
        self.fields['formy'].label = '{0:d}. Wybierz formy uzyskania ocen cząstkowych na kursie:'.format(i)
        i += 1

        for form in FORMS:
            t_name = '{}_t'.format(form[0])
            self.fields[t_name] = ChoiceField(choices=TYPES, required=False)
            for c in comp:
                if form[0] == enum_form[c.form]:
                    self.fields[t_name] = ChoiceField(choices=TYPES, required=False, initial=enum_type[c.type])
            self.fields[t_name].label = '{0:d}. Zaznacz rodzaj oceniania formy: {1}'.format(i, form[0])
            i += 1

        self.fields['mod_plus'] = ChoiceField(choices=YN, initial='Nie')
        self.fields['mod_plus_t'] = ChoiceField(choices=TYPES, required=False)
        self.fields['mod_plus_w'] = FloatField(min_value=0, required=False)
        if mod:
            for m in mod:
                if m.mod == 'PLUS':
                    self.fields['mod_plus'] = ChoiceField(choices=YN, initial='Tak')
                    t = enum_type[m.type]
                    self.fields['mod_plus_t'] = ChoiceField(choices=TYPES, required=False, initial=t)
                    self.fields['mod_plus_w'] = FloatField(min_value=0, required=False, initial=m.val)

        self.fields['mod_plus'].label = '{0:d}. Czy możliwe jest podwyższenie oceny?'.format(i)
        i += 1
        self.fields['mod_plus_t'].label = 'Wybierz w jakim typie jest modyfikacja oceny:'
        self.fields['mod_plus_w'].label = 'Wpisz o ile ocena może zostać podwyższona:'

        self.fields['mod_minus'] = ChoiceField(choices=YN, initial='Nie')
        self.fields['mod_minus_t'] = ChoiceField(choices=TYPES, required=False)
        self.fields['mod_minus_w'] = FloatField(min_value=0, required=False)
        if mod:
            for m in mod:
                if m.mod == 'MINUS':
                    self.fields['mod_minus'] = ChoiceField(choices=YN, initial='Tak')
                    t = enum_type[m.type]
                    self.fields['mod_minus_t'] = ChoiceField(choices=TYPES, required=False, initial=t)
                    self.fields['mod_minus_w'] = FloatField(min_value=0, required=False, initial=m.val)
        self.fields['mod_minus'].label = '{0:d}. Czy możliwe jest obniżenie oceny?'.format(i)
        i += 1
        self.fields['mod_minus_t'].label = 'Wybierz w jakim typie jest modyfikacja oceny:'
        self.fields['mod_minus_w'].label = 'Wpisz o ile ocena może zostać obniżona:'


class CourseGroupForm(Form):

    def __init__(self, *args, **kwargs):
        self.cid = kwargs.pop('course_id')
        self.course_id = Course.objects.get_record_by_id(self.cid)
        super().__init__(*args, **kwargs)
        YN = (
            ('Tak', 'Tak'),
            ('Nie', 'Nie')
        )
        self.fields['if_cg'] = ChoiceField(choices=YN)
        self.fields['if_cg'].label = '1. Czy kurs jest częścią grupy kursów?'

        COURSES = (
            ('ćwiczenia', 'ćwiczenia'),
            ('laboratorium', 'laboratorium'),
        )
        self.fields['courses'] = MultipleChoiceField(widget=CheckboxSelectMultiple, choices=COURSES, required=False)
        self.fields['courses'].label = '2. Zaznacz formy, w których odbywają się zajęcia w ramach grupy kursów:'

        self.fields['weight_c'] = FloatField(min_value=0, max_value=1, required=False)
        self.fields['weight_c'].label = '3. Wpisz udział oceny z ćwiczeń w ocenie końcowej z grupy kursów:'

        self.fields['weight_l'] = FloatField(min_value=0, max_value=1, required=False)
        self.fields['weight_l'].label = '4. Wpisz udział oceny z laboratorium w ocenie końcowej z grupy kursów:'

        self.fields['weight_w'] = FloatField(min_value=0, max_value=1, required=False)
        self.fields['weight_w'].label = '5. Wpisz udział oceny z wykładu w ocenie końcowej z grupy kursów:'

        self.fields['minimum'] = ChoiceField(choices=YN)
        self.fields['minimum'].label = '6. Czy oceny z wszystkich kursów wchodzących w grupę muszą być większe niż 2?'

        for key in self.fields:
            self.fields[key].error_messages['required'] = 'To pole jest wymagane.'
            if 'invalid' in self.fields[key].error_messages:
                self.fields[key].error_messages['invalid'] = 'To nie jest poprawna wartość'
            if 'min_value' in self.fields[key].error_messages:
                self.fields[key].error_messages['min_value'] = 'To nie jest poprawna wartość'
            if 'max_value' in self.fields[key].error_messages:
                self.fields[key].error_messages['max_value'] = 'To nie jest poprawna wartość'

    def clean(self):
        if self.cleaned_data['if_cg'] == 'Tak' and self.cleaned_data['courses'] is None:
            raise ValidationError('W grupie muszą być jakieś kursy oprócz wykładu')

        if self.cleaned_data['weight_c'] is None and 'ćwiczenia' in self.cleaned_data['courses']:
            raise ValidationError('Podaj wagę oceny z ćwiczeń')

        if self.cleaned_data['weight_l'] is None and 'laboratorium' in self.cleaned_data['courses']:
            raise ValidationError('Podaj wagę oceny z laboratorum')

        if self.cleaned_data['weight_w'] is None:
            raise ValidationError('Podaj wagę oceny z ćwiczeń')

        sum = self.cleaned_data['weight_w']
        if 'laboratorium' in self.cleaned_data['courses']:
            sum += self.cleaned_data['weight_l']

        if 'ćwiczenia' in self.cleaned_data['courses']:
            sum += self.cleaned_data['weight_c']

        if sum < 0.99 or sum > 1.01:
            raise ValidationError('Wagi muszą sumować się do 1')

    def save(self):
        if self.cleaned_data['if_cg'] == 'Tak' and not CourseGroup.objects.get_records_by_course_id(self.course_id):
            if self.cleaned_data['minimum'] == 'Tak':
                minimum = True
            else:
                minimum = False
            CourseGroup.objects.add_record(self.course_id, self.cleaned_data['weight_w'], minimum)
            all_types = Course.objects.get_all_types_by_id(self.cid)
            for i in range(len(all_types)):
                if all_types[i].type == 'C':
                    ex = all_types[i]
                elif all_types[i].type == 'L':
                    l = all_types[i]
            if 'ćwiczenia' in self.cleaned_data['courses']:
                CourseGroup.objects.add_record(ex, self.cleaned_data['weight_c'], minimum)

            if 'laboratorium' in self.cleaned_data['courses']:
                CourseGroup.objects.add_record(l, self.cleaned_data['weight_l'], minimum)
