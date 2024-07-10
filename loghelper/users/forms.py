from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

CLASS_FORM_INPUT = {'class': 'form-input-auth'}

PASSWORD = 'password'
PASSWORD2 = 'password2'
LOGIN_PASSWORD = (PASSWORD, PASSWORD2)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs=CLASS_FORM_INPUT)
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs=CLASS_FORM_INPUT)
    )

    class Meta:
        model = get_user_model()
        fields = LOGIN_PASSWORD


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs=CLASS_FORM_INPUT)
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs=CLASS_FORM_INPUT)
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs=CLASS_FORM_INPUT)
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', PASSWORD2)
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs=CLASS_FORM_INPUT),
            'first_name': forms.TextInput(attrs=CLASS_FORM_INPUT),
            'last_name': forms.TextInput(attrs=CLASS_FORM_INPUT),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует')
        return email
