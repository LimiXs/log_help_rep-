from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig

from info_assist.models import ERIPDataBase, DocumentInfo
from info_assist.tables import ERIPFilter, ERIPTable, DocumentInfoTable, DocumentInfoFilter
from info_assist.utils import menu


def home(request):
    """
    View function for home page of site.
    """
    return render(request, 'info_assist/home.html', context={'menu': menu})


def doc_info(request):
    """
    Представление для отображения списка документов.

    Параметры:
    request (django.http.HttpRequest): Объект запроса Django.

    Возвращает:
    django.http.HttpResponse: Отрендеренный HTML-шаблон с информацией о документах.
    """
    # Получаем все объекты DocumentInfo из базы данных
    queryset = DocumentInfo.objects.all()

    # Проверяем, есть ли в запросе параметр 'pdf_only'
    pdf_only = request.GET.get('pdf_only')

    # Если параметр 'pdf_only' равен 'true', фильтруем queryset, оставляя только документы с заполненным pdf_blob
    if pdf_only == 'true':
        queryset = queryset.filter(pdf_blob__isnull=False)

    # Создаем фильтр для queryset на основе параметров запроса
    document_filter = DocumentInfoFilter(request.GET, queryset=queryset)

    # Создаем таблицу для отображения документов, сортируя ее по параметру 'sort' из запроса
    table = DocumentInfoTable(document_filter.qs, order_by=request.GET.get('sort'))

    # Настраиваем пагинацию таблицы, отображая по 10 записей на странице
    RequestConfig(request, paginate={'per_page': 12}).configure(table)

    # Возвращаем отрендеренный HTML-шаблон с информацией о документах
    return render(
        request,
        'info_assist/doc_info.html',
        {
            'table': table, 'filter': document_filter,
            'title': 'Документы', 'pdf_only': pdf_only
        },
    )


def erip_info(request):
    erip_filter = ERIPFilter(request.GET, queryset=ERIPDataBase.objects.all())
    table = ERIPTable(erip_filter.qs)
    RequestConfig(request, paginate={'per_page': 12}).configure(table)
    return render(
        request,
        'info_assist/erip_info.html',
        {'table': table, 'filter': erip_filter, 'title': 'ERIP'},
    )


def download_pdf(request, pk):
    document = get_object_or_404(DocumentInfo, pk=pk)
    if document.pdf_blob:
        response = HttpResponse(document.pdf_blob, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{document.num_item}.pdf"'
        return response
    else:
        return HttpResponse("Файл не найден", status=404)


def test(request):
    return render(request, 'info_assist/test.html')


def page_not_found(request, exception):
    """
    Custom 404 error handler.
    """
    return render(request, 'info_assist/404.html', status=404)
