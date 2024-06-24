from django.urls import path
from info_assist import views

urlpatterns = [
    path('', views.index),
]