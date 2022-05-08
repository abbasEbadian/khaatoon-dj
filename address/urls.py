from django.urls import path
from . import views 

urlpatterns = [
    path('edit/', views.edit_address),
    path('create/', views.create_address),

]