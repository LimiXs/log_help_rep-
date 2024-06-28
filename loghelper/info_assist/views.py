from django.shortcuts import render
from django_tables2 import RequestConfig

from info_assist.models import ERIPDataBase, DocumentInfo
from info_assist.tables import ERIPFilter, ERIPTable, DocumentInfoTable

menu = [
    {'title': 'Уведомления', 'url_name': 'doc_info'},
    {'title': 'ERIP', 'url_name': 'erip_info'},
]


def erip_info(request):
    erip_filter = ERIPFilter(request.GET, queryset=ERIPDataBase.objects.all())
    table = ERIPTable(erip_filter.qs)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(
        request,
        'info_assist/erip_info.html',
        {'table': table, 'filter': erip_filter, 'menu': menu},
    )


def home(request):
    """
    View function for home page of site.
    """
    return render(request, 'info_assist/home.html', context={'menu': menu})


# def erip_info(request):
#     data['title'] = 'ERIP'
#     return render(request, 'info_assist/erip_info.html', context=data)


def doc_info(request):
    filter_value = request.GET.get('num_item', None)
    date_value = request.GET.get('date_placement', None)

    queryset = DocumentInfo.objects.all()

    if filter_value:
        queryset = queryset.filter(num_item__icontains=filter_value)

    if date_value:
        queryset = queryset.filter(date_placement=date_value)

    table = DocumentInfoTable(queryset)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)

    context = {
        'table': table,
        'title': 'Уведомления',
        'menu': menu
    }

    return render(request, 'info_assist/doc_info.html', context)


def test(request):
    return render(request, 'info_assist/test.html', context={'menu': menu})


def page_not_found(request, exception):
    """
    Custom 404 error handler.
    """
    return render(request, '404.html', status=404)
