from django.urls import path, include
from . import views
urlpatterns = [
    path('market/all/', views.get_market_chats),
    path('user/all/', views.get_user_chats),
    path('send/', views.send_message),
    path('market/seen/', views.seen_message_from_market),
    path('user/seen/', views.seen_message_from_user),
    path('user/create/', views.create_message_for_user),
    path('market/create/', views.create_message_for_market),

]