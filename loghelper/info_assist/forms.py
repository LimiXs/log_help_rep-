# forms.py
from django import forms
from info_assist.models import PDFDataBase


class PDFDataBaseAdminForm(forms.ModelForm):
    class Meta:
        model = PDFDataBase
        fields = '__all__'

    # Add a field for file upload
    new_pdf_file = forms.FileField(required=False, label='Загрузить новый PDF файл')