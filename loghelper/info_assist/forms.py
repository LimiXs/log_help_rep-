# forms.py
from django import forms

from info_assist.models import PDFDataBase


class ExtraButtonsForm(forms.Form):
    button1 = forms.CharField(label='Кнопка 1', max_length=100, widget=forms.HiddenInput())
    button2 = forms.CharField(label='Кнопка 2', max_length=100, widget=forms.HiddenInput())
    button3 = forms.CharField(label='Кнопка 3', max_length=100, widget=forms.HiddenInput())


class PDFDataBaseAdminForm(forms.ModelForm):
    class Meta:
        model = PDFDataBase
        fields = '__all__'

    # Add a field for file upload
    new_pdf_file = forms.FileField(required=False, label='Загрузить новый PDF файл')