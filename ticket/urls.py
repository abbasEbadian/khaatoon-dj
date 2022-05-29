from django.urls import path
from . import views 
urlpatterns = [
    path('add_ticket/', views.add_ticket),
    path('add_message/', views.add_message),
    path('close/', views.close_ticket),
    path('close_admin/<int:pk>', views.close_ticket_admin),
    path('seen/<int:pk>/', views.seen),
    path('send_contact_us_message/', views.send_contact_us_message)
]