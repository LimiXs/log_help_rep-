from django.shortcuts import render

menu = [
    {'title': 'Уведомления', 'url_name': 'doc_info'},
    {'title': 'ERIP', 'url_name': 'erip_info'},
]

data = {
        'menu': menu
    }


def home(request):
    """
    View function for home page of site.
    """
    data['title'] = 'Главная страница'
    return render(request, 'info_assist/home.html', context=data)


def erip_info(request):
    data['title'] = 'ERIP'
    return render(request, 'info_assist/erip_info.html', context=data)


def doc_info(request):
    data['title'] = 'Уведомления'
    return render(request, 'info_assist/doc_info.html', context=data)


def page_not_found(request, exception):
    """
    Custom 404 error handler.
    """
    return render(request, '404.html', status=404)
