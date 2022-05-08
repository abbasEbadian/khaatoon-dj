from django.urls import path
from . import views 

urlpatterns = [
    path('deposit/url', views.get_deposit_url)
]