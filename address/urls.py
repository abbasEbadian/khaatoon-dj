from django.urls import path
from . import views 

urlpatterns = [
    path('edit/', views.edit_address),
    path('create/', views.create_address),
    path('delete/<int:pk>/', views.delete),
    path('change_active/<int:pk>/', views.change_active),

]