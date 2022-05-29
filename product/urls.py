from django.urls import path, include
from . import views

urlpatterns = [
    path('all/', views.get_all_products),
    path('search_with_name/', views.search_with_name),
    path('<int:pk>/', views.get_product_by_id),
    path('category/<int:pk>/', views.get_products_by_category_id),
    path('create/', views.create_product),
    path('update/', views.update_product),
    path('update_visibility/', views.update_visibility),
    path('delete/<int:pk>', views.delete_product),
    path('index/', views.get_index_products),
    

]