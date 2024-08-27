from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('button-action/<str:action>/', views.button_action, name='button_action'),
    path('erip-info/', views.erip_info, name='erip_info'),
    path('doc-info/', views.doc_info, name='doc_info'),
    path('download_pdf/<int:pk>/', views.download_pdf, name='download_pdf'),
    path('test/', views.test, name='test'),
]
