# tables.py
from django import forms
from django_filters import FilterSet, CharFilter, DateFromToRangeFilter, DateFilter
from .models import DocumentInfo, ERIPDataBase
import django_tables2 as tables

TABLE_ATTRS = {'class': 'table table-sm'}
INPUT_ATTRS = {'class': 'form-control'}

TEMPLATE_NAME = 'django_tables2/bootstrap.html'
FORMAT_DATE = {'placeholder': 'dd/mm/yyyy', 'format': '%d/%m/%Y', 'max_length': 10}


class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({**INPUT_ATTRS, **FORMAT_DATE})
        super().__init__(*args, **kwargs)


class DocumentInfoTable(tables.Table):
    download = tables.TemplateColumn(
        template_name='info_assist/download_button.html',
        verbose_name='Скачать',
        orderable=True,
        order_by=('pdf_file',)
    )

    class Meta:
        model = DocumentInfo
        attrs = TABLE_ATTRS
        template_name = TEMPLATE_NAME
        fields = (
            'date_placement',
            'num_item',
            'num_transport',
            'status',
            'num_nine',
            'num_td',
            'download'
        )
        sequence = (
            'date_placement', 'num_item', 'num_transport', 'num_doc',
            'date_docs', 'status', 'num_nine', 'num_td',
        )
        exclude = ('path_doc', 'documents', 'num_doc', 'date_docs')
        order_by = ('-date_placement',)



class DocumentInfoFilter(FilterSet):
    num_item = CharFilter(
        field_name='num_item',
        lookup_expr='iregex',
        label='№ УВР',
        widget=forms.TextInput(attrs=INPUT_ATTRS),
    )
    num_transport = CharFilter(
        field_name='num_transport',
        lookup_expr='iregex',
        label='№ авто',
        widget=forms.TextInput(attrs=INPUT_ATTRS),
    )
    date_placement = DateFilter(
        field_name='date_placement',
        widget=DateInput(),
        label='Дата',
    )

    class Meta:
        model = DocumentInfo
        fields = ['num_item', 'num_transport', 'date_placement']
        order_by = ['-date_placement']


class ERIPTable(tables.Table):
    class Meta:
        model = ERIPDataBase
        attrs = TABLE_ATTRS
        template_name = TEMPLATE_NAME
        fields = (
            'id_account',
            'payer_name',
            'bill_pay',
            'date',
        )
        show_footer = False


class ERIPFilter(FilterSet):
    id_account = CharFilter(
        field_name='id_account',
        lookup_expr='icontains',
        label='Счёт договора'
    )
    payer_name = CharFilter(
        field_name='payer_name',
        lookup_expr='iregex',
        label='Ф.И.О плательщика'
    )
    date = DateFromToRangeFilter(
        widget=DateInput(),
        label='Дата оплаты'
    )

    class Meta:
        model = ERIPDataBase
        fields = ['id_account', 'payer_name', 'date']
