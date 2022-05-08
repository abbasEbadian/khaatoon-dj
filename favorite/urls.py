from django.urls import path, include
from . import views


urlpatterns = [
    path('toggle/', views.toggle),
]