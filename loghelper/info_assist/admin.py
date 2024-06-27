from django.contrib import admin, messages
from django.db import connection
from django.http import HttpResponseRedirect
from admin_extra_buttons.api import ExtraButtonsMixin, button

from .external_utils.connecter_fdb import get_data_fdb, HOSTNAME, DATABASE_PATH, USERNAME, PASSWORD
from .scheduler import match_pdfs_docs, upload_docs_db, Scheduler
from .management.commands.read_files_erip import Command
from .utils import MAPPING

from info_assist.models import *


@admin.register(DocumentInfo)
class DocumentInfoAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = [field.name for field in DocumentInfo._meta.get_fields()]
    list_display_links = ('id', 'num_item',)
    list_filter = ('num_item',)
    search_fields = ('num_item',)
    list_per_page = 6

    scheduler = Scheduler()

    @button(
        label='Загрузить данные',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def load_data(self, request):
        records = get_data_fdb(HOSTNAME, DATABASE_PATH, USERNAME, PASSWORD)
        for record in records:
            if not DocumentInfo.objects.filter(num_item=record[0]).exists():
                DocumentInfo.objects.create(
                    date_placement=record[1],
                    num_item=record[0],
                    num_transport=record[3].replace(';', '; '),
                    num_doc=record[4],
                    date_docs=record[7],
                    documents=record[6],
                    status=record[9],
                    num_nine=record[10],
                    num_td=record[11] if record[11] is None else record[11][:30].replace(';', '; ')
                )

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @button(
        label='Запустить планировщик',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def admin_start_scheduler(self, request):
        self.scheduler.start_scheduler(
            {'func': match_pdfs_docs, 'interval': 10},
            {'func': upload_docs_db, 'interval': 15}
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @button(
        label='Остановить планировщик',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def admin_stop_scheduler(self, request):
        self.scheduler.stop_scheduler()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@admin.register(ERIPDataBase)
class ERIPDataBaseAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = [field.name for field in ERIPDataBase._meta.get_fields()]
    list_display_links = ('id', 'id_account',)
    search_fields = ('id_account',)

    @button(label='Удалить всё и сбросить автоинкремент', change_form=True, html_attrs={"class": 'btn-primary'})
    def delete_all_and_reset(self, request):
        ERIPDataBase.objects.all().delete()
        self.message_user(request, "Все данные успешно удалены", level=messages.SUCCESS)

        table_name = ERIPDataBase._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
        self.message_user(request, "Автоинкремент успешно сброшен", level=messages.SUCCESS)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @button(label='Загрузить данные', change_form=True, html_attrs={"class": 'btn-primary'})
    def load_data(self, request):
        Command().handle()
        self.message_user(request, "Данные успешно загружены", level=messages.SUCCESS)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@admin.register(PDFDataBase)
class PDFDataBaseAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = [field.name for field in PDFDataBase._meta.fields]
    list_display_links = ('id',)

    @button(
        label='Обновить символы',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def update_chars(self, request):
        records = PDFDataBase.objects.all()
        for record in records:
            for english_char, russian_char in MAPPING.items():
                record.doc_number = record.doc_number.replace(english_char, russian_char)
            record.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
