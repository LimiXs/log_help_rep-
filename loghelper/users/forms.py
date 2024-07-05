from django import forms

CLASS_FORM_INPUT = {'class': 'form-input'}


class LoginUserForm(forms.Form):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs=CLASS_FORM_INPUT)
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs=CLASS_FORM_INPUT)
    )
