from django.urls import path, include
from . import views

urlpatterns = [
    path('all/', views.get_all_attributes),
]