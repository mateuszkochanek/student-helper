from django.forms import Form, CheckboxSelectMultiple, MultipleChoiceField, FloatField, ChoiceField
from studentHelper.models import Components, Thresholds, CourseGroup, Modyfication, Course


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
