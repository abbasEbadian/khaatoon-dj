from django.urls import path, include
from . import views

urlpatterns = [
    path('province/all/', views.get_province_all),
    path('city/province/<int:pk>', views.get_cities_by_province),
]