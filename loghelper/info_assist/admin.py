from django.contrib import admin, messages
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html

from .scheduler import Scheduler
from .tasks import *
from .management.commands.read_files_erip import Command
from .utils import MAPPING

from admin_extra_buttons.api import ExtraButtonsMixin, button
from info_assist.models import *


class PDFFileFilter(admin.SimpleListFilter):
    title = 'Наличие PDF файла'
    parameter_name = 'has_pdf'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'С PDF файлом'),
            ('no', 'Без PDF файла'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(pdf_file__isnull=False)
        if self.value() == 'no':
            return queryset.filter(pdf_file__isnull=True)
        return queryset


@admin.register(DocumentInfo)
class DocumentInfoAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    scheduler = Scheduler()
    list_display = (
        'id',
        'date_placement',
        'num_item',
        'num_transport',
        'status',
        'num_nine',
        'num_td',
        'download_pdf',  # Добавляем поле для скачивания PDF
    )
    list_display_links = ('id', 'num_item')
    search_fields = ('num_item', 'num_transport')
    list_per_page = 10
    list_filter = (PDFFileFilter,)  # Добавляем фильтр

    @button(
        label='Загрузить данные',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def load_data(self, request):
        link_pdf_to_documents()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @button(
        label='Остановить планировщик',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def admin_stop_scheduler(self, request):
        self.scheduler.stop_scheduler()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def download_pdf(self, obj):
        if hasattr(obj, 'pdf_file') and obj.pdf_file:
            return f'<a href="{obj.pdf_file.full_path}" download>Скачать PDF</a>'
        return 'Нет PDF файла'

    download_pdf.allow_tags = True  # Позволяем HTML в поле
    download_pdf.short_description = 'Скачать PDF файл'  # Заголовок столбца


@admin.register(ERIPDataBase)
class ERIPDataBaseAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = [field.name for field in ERIPDataBase._meta.get_fields()]
    list_display_links = ('id', 'id_account',)
    search_fields = ('id_account',)

    @button(
        label='Удалить всё и сбросить автоинкремент',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def delete_all_and_reset(self, request):
        ERIPDataBase.objects.all().delete()
        self.message_user(request, "Все данные успешно удалены", level=messages.SUCCESS)

        table_name = ERIPDataBase._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
        self.message_user(request, "Автоинкремент успешно сброшен", level=messages.SUCCESS)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @button(
        label='Загрузить данные',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def load_data(self, request):
        Command().handle()
        self.message_user(request, "Данные успешно загружены", level=messages.SUCCESS)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@admin.register(PDFDataBase)
class PDFDataBaseAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = [field.name for field in PDFDataBase._meta.fields]
    list_display_links = ('id',)

    @button(
        label='Парсинг и Загрузка',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def scan_and_load(self, request):
        scan_and_load_pdfs()
        # link_pdf_to_documents()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @button(
        label='Удалить всё и сбросить автоинкремент',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def delete_all_and_reset(self, request):
        PDFDataBase.objects.all().delete()
        self.message_user(request, "Все данные успешно удалены", level=messages.SUCCESS)

        table_name = PDFDataBase._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
        self.message_user(request, "Автоинкремент успешно сброшен", level=messages.SUCCESS)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
