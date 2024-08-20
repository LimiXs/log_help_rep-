from django_tables2 import RequestConfig
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from info_assist.utils import menu
from info_assist.models import ERIPDataBase, DocumentInfo
from info_assist.tables import ERIPFilter, ERIPTable, DocumentInfoTable, DocumentInfoFilter
from info_assist.tasks import link_pdf_to_documents, upload_docs_db, scan_and_load_pdfs


@login_required
def button_action(request, action):
    """
    View function to handle different button actions.
    """
    try:
        if action == 'link_pdf':
            link_pdf_to_documents()
            messages.success(request, "PDFs successfully linked to documents.")
        elif action == 'upload_docs':
            upload_docs_db()
            messages.success(request, "Documents uploaded to database successfully.")
        elif action == 'scan_and_load':
            scan_and_load_pdfs()
            messages.success(request, "PDFs scanned and loaded successfully.")
        else:
            messages.error(request, "Invalid action.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect('home')

@login_required
def home(request):
    """
    View function for home page of site.
    """
    context = {
        'menu': menu,  # Если у вас есть меню
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
        pdf_blob = document.pdf_file.blob
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
