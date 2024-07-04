import django_tables2 as tables
from django import forms

from .models import DocumentInfo, ERIPDataBase
from django_filters import FilterSet, CharFilter, DateFromToRangeFilter, DateFilter

ATTRS = {'class': 'table table-sm'}
TEMPLATE_NAME = 'django_tables2/bootstrap.html'
WIDGET_ATTR = {'placeholder': 'DD/MM/YYYY', 'max_length': 10}


class DateInput(forms.DateInput):
    input_type = 'date'


class DocumentInfoTable(tables.Table):
    download = tables.TemplateColumn(
        template_name='info_assist/download_button.html',
        verbose_name='Скачать',
        orderable=True,
        order_by=('pdf_blob',)  # Указываем поле для сортировки
    )

    class Meta:
        model = DocumentInfo
        attrs = ATTRS
        template_name = TEMPLATE_NAME
        fields = (
            'date_placement',
            'num_item',
            'num_transport',
            'status',
            'num_nine',
            'num_td',
            'download'  # Включаем столбец "Скачать"
        )
        sequence = (
            'date_placement', 'num_item', 'num_transport', 'num_doc',
            'date_docs', 'status', 'num_nine', 'num_td', 'download'
        )
        exclude = ('path_doc', 'documents', 'num_doc', 'date_docs')


class DocumentInfoFilter(FilterSet):
    num_item = CharFilter(field_name='num_item', lookup_expr='icontains', label='№ УВР')
    date_placement = DateFilter(
        field_name='date_placement',
        widget=DateInput(attrs=WIDGET_ATTR),
        label='Дата'
    )

    class Meta:
        model = DocumentInfo
        fields = ['num_item', 'date_placement']


class ERIPTable(tables.Table):
    class Meta:
        model = ERIPDataBase
        attrs = ATTRS
        template_name = TEMPLATE_NAME
        fields = (
            'id_account',
            'payer_name',
            'bill_pay',
            'date',
        )
        show_footer = False


class ERIPFilter(FilterSet):
    id_account = CharFilter(field_name='id_account', lookup_expr='icontains', label='Счёт договора')
    payer_name = CharFilter(field_name='payer_name', lookup_expr='icontains', label='ФИО плательщика')
    date = DateFromToRangeFilter(
        widget=DateInput(attrs=WIDGET_ATTR),
        label='Дата оплаты'
    )

    class Meta:
        model = ERIPDataBase
        fields = ['id_account', 'payer_name', 'date']
