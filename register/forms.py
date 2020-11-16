from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login"
        self.fields["username"].help_text = "Wymagane. Dozwolone znaki to litery, cyfry oraz @/./+/-/_."
        self.fields["first_name"].label = "Imię"
        self.fields["last_name"].label = "Nazwisko"
        self.fields["password1"].label = "Hasło"
        self.fields["password2"].label = "Powtórz hasło"
        self.fields[
            'password1'].help_text = "<ul><li>Hasło nie może być podobne do innych Twoich danych.</li><li>Hasło musi " \
                                     "mieć conajmniej 8 znaków.</li><li>Hasło nie może być popularnym " \
                                     "hasłem.</li><li>Hasło nie może składać się z samych cyfr.</li></ul> "
        self.fields["password2"].help_text = "Powtórz hasło dla weryfikacji."
        for key in self.fields:
            self.fields[key].error_messages['required'] = "To pole jest wymagane."