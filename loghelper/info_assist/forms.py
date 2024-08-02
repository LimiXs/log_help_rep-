# forms.py
from django import forms


class ExtraButtonsForm(forms.Form):
    button1 = forms.CharField(label='Кнопка 1', max_length=100, widget=forms.HiddenInput())
    button2 = forms.CharField(label='Кнопка 2', max_length=100, widget=forms.HiddenInput())
    button3 = forms.CharField(label='Кнопка 3', max_length=100, widget=forms.HiddenInput())
