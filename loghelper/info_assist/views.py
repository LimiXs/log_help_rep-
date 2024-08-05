from cryptography.fernet import Fernet
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from info_assist.forms import ExtraButtonsForm
from info_assist.models import ERIPDataBase, DocumentInfo
from info_assist.tables import ERIPFilter, ERIPTable, DocumentInfoTable, DocumentInfoFilter
from info_assist.utils import menu
from loghelper.settings._base import CRYPTO_KEY


@login_required
def home(request):
    """
    View function for home page of site.
    """
    if request.user.is_authenticated:
        buttons_form = ExtraButtonsForm(initial={
            'button1': {'label': 'Кнопка 1', 'url': reverse('home')},
            'button2': {'label': 'Кнопка 2', 'url': reverse('home')},
            'button3': {'label': 'Кнопка 3', 'url': reverse('home')},
        })
        buttons = [
            {'label': 'Кнопка 1', 'url': reverse('home')},
            {'label': 'Кнопка 2', 'url': reverse('home')},
            {'label': 'Кнопка 3', 'url': reverse('home')}
        ]
    else:
        buttons_form = None
        buttons = None

    context = {
        'menu': menu,
        'buttons_form': buttons_form,
        'buttons': buttons
    }
    return render(request, 'info_assist/home.html', context=context)


@login_required
def doc_info(request):
    queryset = DocumentInfo.objects.all()
    pdf_only = request.GET.get('pdf_only')

    if pdf_only == 'true':
        queryset = queryset.filter(pdf_file__isnull=False)

    document_filter = DocumentInfoFilter(request.GET, queryset=queryset)
    table = DocumentInfoTable(document_filter.qs, order_by=request.GET.get('sort'))
    RequestConfig(request, paginate={'per_page': 12}).configure(table)

    return render(
        request,
        'info_assist/doc_info.html',
        {
            'table': table, 'filter': document_filter,
            'title': 'Документы', 'pdf_only': pdf_only
        },
    )


@login_required
def erip_info(request):
    erip_filter = ERIPFilter(request.GET, queryset=ERIPDataBase.objects.all())
    table = ERIPTable(erip_filter.qs)
    RequestConfig(request, paginate={'per_page': 12}).configure(table)
    return render(
        request,
        'info_assist/erip_info.html',
        context={'table': table, 'filter': erip_filter, 'title': 'ERIP'},
    )


@login_required
def download_pdf(request, pk):
    document = get_object_or_404(DocumentInfo, pk=pk)
    # if document.pdf_file:
    #     response = HttpResponse(document.pdf_file, content_type='application/pdf')
    #     response['Content-Disposition'] = f'attachment; filename="{document.num_item}.pdf"'
    #     return response
    # else:
    #     return HttpResponse("Файл не найден", status=404)
    if document.pdf_file:
        pdf_data = document.pdf_file.blob
        cipher = Fernet(CRYPTO_KEY)
        pdf_blob = cipher.decrypt(pdf_data)
        response = HttpResponse(pdf_blob, content_type='application/pdf')
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
