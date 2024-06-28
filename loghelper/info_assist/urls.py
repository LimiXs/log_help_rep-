from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('erip-info/', views.erip_info, name='erip_info'),
    path('doc-info/', views.doc_info, name='doc_info'),
    path('test/', views.test, name='test'),
]

