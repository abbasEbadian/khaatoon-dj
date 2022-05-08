from django.urls import path, include
from . import views

urlpatterns = [
    path('all/', views.get_all_products),
    path('<int:pk>/', views.get_product_by_id),
    path('category/<int:pk>/', views.get_products_by_category_id),
    

]