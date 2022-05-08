from django.urls import path, include
from . import views
urlpatterns = [
    # path('market/<int:pk>/', views.get_market_data),
    # path('market/business/all/', views.get_all_businesses),
    path('business_and_province/all/', views.get_all_business_and_province),
]