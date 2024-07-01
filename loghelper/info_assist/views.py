from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig

from info_assist.models import ERIPDataBase, DocumentInfo
from info_assist.tables import ERIPFilter, ERIPTable, DocumentInfoTable, DocumentInfoFilter

menu = [
    {'title': 'Уведомления', 'url_name': 'doc_info'},
    {'title': 'ERIP', 'url_name': 'erip_info'},
]


def home(request):
    """
    View function for home page of site.
    """
    return render(request, 'info_assist/home.html', context={'menu': menu})


def doc_info(request):
    queryset = DocumentInfo.objects.all()
    pdf_only = request.GET.get('pdf_only')

    if pdf_only == 'true':
        queryset = queryset.filter(pdf_blob__isnull=False)

    document_filter = DocumentInfoFilter(request.GET, queryset=queryset)

    table = DocumentInfoTable(document_filter.qs, order_by=request.GET.get('sort'))
    RequestConfig(request, paginate={'per_page': 10}).configure(table)

    return render(
        request,
        'info_assist/doc_info.html',
        {
            'table': table, 'filter': document_filter, 'menu': menu,
            'title': 'Документы', 'pdf_only': pdf_only
        },
    )


def download_pdf(request, pk):
    document = get_object_or_404(DocumentInfo, pk=pk)
    if document.pdf_blob:
        response = HttpResponse(document.pdf_blob, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{document.num_item}.pdf"'
        return response
    else:
        return HttpResponse("Файл не найден", status=404)


def erip_info(request):
    erip_filter = ERIPFilter(request.GET, queryset=ERIPDataBase.objects.all())
    table = ERIPTable(erip_filter.qs)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(
        request,
        'info_assist/erip_info.html',
        {'table': table, 'filter': erip_filter, 'menu': menu},
    )


def test(request):
    return render(request, 'info_assist/test.html', context={'menu': menu})


def page_not_found(request, exception):
    """
    Custom 404 error handler.
    """
    return render(request, '404.html', status=404)
