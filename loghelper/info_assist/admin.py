from django.contrib import admin, messages
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html

from .forms import PDFDataBaseAdminForm
from .scheduler import start_scheduler, stop_scheduler
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
    def admin_load_data(self, request):
        link_pdf_to_documents()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @button(
        label='Запустить планировщик',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def admin_start_scheduler(self, request):
        start_scheduler()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @button(
        label='Остановить планировщик',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def admin_stop_scheduler(self, request):
        stop_scheduler()
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


#
# @admin.register(PDFDataBase)
# class PDFDataBaseAdmin(ExtraButtonsMixin, admin.ModelAdmin):
#     list_display = [field.name for field in PDFDataBase._meta.fields]
#     list_display_links = ('id',)
#
#

class PDFDataBaseAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    form = PDFDataBaseAdminForm

    list_display = (
        'id',
        'doc_number',
        'full_path',
        'file_name',
        'status',
        'created_at',
        'updated_at',
        'download_link',
    )
    list_display_links = ('id',)

    def download_link(self, obj):
        if obj.blob:
            return format_html('<a href="{}">Скачать PDF</a>', self.get_download_url(obj.id))
        return "Нет файла"

    download_link.short_description = 'Ссылка на PDF'

    def get_download_url(self, object_id):
        return f'/admin/info_assist/pdfdatabase/{object_id}/download_pdf/'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/download_pdf/', self.admin_site.admin_view(self.download_pdf), name='download_pdf'),
            path('<int:object_id>/clear_pdf/', self.admin_site.admin_view(self.clear_pdf), name='clear_pdf'),
        ]
        return custom_urls + urls

    def download_pdf(self, request, object_id):
        pdf_instance = self.get_object(request, object_id)
        if pdf_instance and pdf_instance.blob:
            response = HttpResponse(pdf_instance.blob, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_instance.file_name or "document.pdf"}"'
            return response
        else:
            self.message_user(request, "PDF файл не найден", level=messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def clear_pdf(self, request, object_id):
        pdf_instance = self.get_object(request, object_id)
        if pdf_instance:
            pdf_instance.blob = None
            pdf_instance.save()
            self.message_user(request, "PDF файл успешно очищен", level=messages.SUCCESS)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('new_pdf_file'):
            obj.blob = form.cleaned_data['new_pdf_file']
        super().save_model(request, obj, form, change)

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return ['blob']  # Make the blob field read-only
    #     return super().get_readonly_fields(request, obj)

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


admin.site.register(PDFDataBase, PDFDataBaseAdmin)
