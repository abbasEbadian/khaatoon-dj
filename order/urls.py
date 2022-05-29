from django.urls import path
from . import views

urlpatterns = [
    path('get_cart/', views.get_basket),
    path('add_to_cart/', views.add_to_cart),
    path('delete_cart/', views.delete_cart),
    path('increase_cart_item/', views.increase_cart_item),
    path('decrease_cart_item/', views.decrease_cart_item),
    path('remove_cart_item/', views.remove_cart_item),

]