from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string


# Create your views here.
def index(request):
    """
    View function for home page of site.
    """
    return render(request, 'info_assist/index.html')


def test(request):
    print(request.GET)
    return HttpResponse("<h1>Тест</h1>")


def page_not_found(request, exception):
    """
    404 page
    """
    return HttpResponse("<h1>Страница не найдена</h1>")
